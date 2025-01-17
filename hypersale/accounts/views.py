import json
from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, views,viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer, LoginSerializer, LogoutSerializer
from .models import CustomUser
from rest_framework.authentication import TokenAuthentication
from django.views import View
from .forms import LoginForm, RegistrationForm

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            #Generate or retrieve a token for the newly registered user
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer 

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
    
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 
                             'user_id': user.id,
                             'username': user.username},
                             status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        

class LogOutView(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
     
    def post (self, request, *args, **kwargs):
        print("User authenticated:", request.user.is_authenticated)
        print("User token:", request.headers.get('Authorization'))

        if not request.user.is_authenticated:
            return Response ({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        logout (request)

        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        logout_message= ({'message': 'Successfully logged out.'})
        
        serializer = LogoutSerializer(data=logout_message)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


  # Assuming you have a LoginForm defined in forms.py

class Login_View(View):
    template_name = 'login.html'  # Path to your login template

    def get(self, request):
        form = LoginForm()  # Instantiate the form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home or any other page
            else:
                form.add_error(None, "Invalid username or password.")
        return render(request, self.template_name, {'form': form})
    

class RegistrationView(View):
    template_name = 'register.html'  # Path to your registration template

    def get(self, request):
        form = RegistrationForm()  # Instantiate the form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home or any other page
        return render(request, self.template_name, {'form': form})