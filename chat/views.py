from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

class ChatView(APIView):
    authentication_classes = [IsAuthenticated]
    
    def post(self, request, target):
        Users = get_user_model()

        user = Users.objects.filter(pk=int(target)).first()

        print(user)
        
        if user == None:
            return Response({"status":status.HTTP_404_NOT_FOUND,"message":"User does not exist"})
        
        if user.is_online():
            return Response({"status":status.HTTP_200_OK,"message":"User is online, connecting to chat..."})
        else:
            #TODO: check what status code to return for this situation
            return Response({"status":status.HTTP_200_OK, "message":"User is not online, can't send any messages right now"})
        