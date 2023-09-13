from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer
from .recommender import get_suggested_friends

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["user_id"] = user.pk
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class Register(APIView):

    def post(self,request):
        serializer_data = RegisterSerializer(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'status':status.HTTP_201_CREATED ,"result":serializer_data.data})
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'error':serializer_data.errors})

class CustomTokenRefreshView(TokenRefreshView):

    authentication_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.body)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # set Refresh and Access token in browser with Httponly cookie.
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key= "refresh_token",
            value=serializer.validated_data["refresh"],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        return response
    

class OnlineUsers(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):
        print(request.auth)
        Users = get_user_model()

        online_users = Users.objects.filter(online=True)

        print(online_users)

        return Response({"status":status.HTTP_200_OK,"message":f"Users online: {online_users}"})
    

class Login(APIView):

    def post(self,request):

        serializer = LoginSerializer(data = request.data, context={'request': request})

        if serializer.is_valid():
            
            response =  Response({"message":"successfully authenticated user!"})
            #get tokens for user
            username = serializer.validated_data["username"]
            user = get_user_model().objects.filter(username=username).first()
            tokens = get_tokens_for_user(user)

            #user is now online
            user.set_user_online()
            
            #set refresh tokens as cookies
            response.set_cookie(
                    key = "refresh_token", 
                    value = tokens["refresh"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                    )
            response.set_cookie(
                key="user",
                value=user.pk
            )
            response.data["access_token"] = tokens["access"]
            return response
        
        else:
            return Response({'result':serializer.errors})
        
class Logout(APIView):

    authentication_classes = [IsAuthenticated]

    def post(self,request):
        
        try:
            refresh_token = RefreshToken(request.COOKIES['refresh_token'])
            user = get_user_model().objects.filter(pk=request.COOKIES['user']).first()
            user.set_user_offline()
            refresh_token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":f"Error occurred: {e}"})
        
class SuggestedFriendsView(APIView):

    def get(self,request, user_id):

        try:
            suggested_friends = get_suggested_friends(user_id)
            return Response(status=status.HTTP_200_OK, data={"message":f"{suggested_friends}"})

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"error:":e})