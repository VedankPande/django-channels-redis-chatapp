from rest_framework import serializers,status
from django.contrib.auth import authenticate, get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only = True)

    class Meta:
        model = get_user_model()
        fields = "__all__"

    def save(self):

        UserModel = get_user_model()

        password = self.validated_data['password']

        if UserModel.objects.filter(email=self.validated_data['email']):
            raise serializers.ValidationError({'status':status.HTTP_409_CONFLICT, 'error': 'That email is already in use'})
        
        user = UserModel(email = self.validated_data['email'], username = self.validated_data['username'])
        user.set_password(password)
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    username = serializers.CharField(max_length=255)

    def validate(self, data):

        Username = data.get('username')
        Password = data.get('password')

        if Username and Password:
            user = authenticate(username = Username, password= Password)

            if not user:
                raise serializers.ValidationError({'error': 'could not validate that user'})
            
            data['user'] = user
            return data
        
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
