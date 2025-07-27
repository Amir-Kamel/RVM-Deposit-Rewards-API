from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from django.utils import timezone
from .utils import send_otp_email



User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
     def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "No user with this username."})
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"password": "Incorrect password."})
        data = super().validate(attrs)
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return data
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        elif self.request.method == 'GET':
            return [IsAdminUser()]
        return super().get_permissions()

    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response({"response": "No users found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": f"Token error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)




class SendEmailOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        send_otp_email(user)
        return Response({"detail": "OTP sent to your email."}, status=status.HTTP_200_OK)


class VerifyEmailOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp = request.data.get("otp")

        if not otp:
            return Response({"error": "OTP code is required."}, status=status.HTTP_400_BAD_REQUEST)

        expiration_time = user.expired_at
        if user.otp != otp:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        elif expiration_time and timezone.now() > expiration_time:
            return Response({"error": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.otp = ""
        user.expired_at = None
        user.save()

        return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
