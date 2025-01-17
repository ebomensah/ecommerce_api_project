from django.contrib.auth import authenticate, get_user_model
from django.http import request
from rest_framework.response import Response
from .models import CustomUser
from rest_framework import serializers, status 
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}}

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            )
        user.set_password(validated_data['password'])
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        #user.token = token.key
        return user 
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Authenticate user based on username and password
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        # If authentication is successful, return the user and token
        token, created = Token.objects.get_or_create(user=user)
        return {
            'user': user,
            'token': token.key
        }
    
class LogoutSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)

    def create(self, validated_data):
        request.user.auth_token.delete()
        return {"message": "Successfully logged out."}