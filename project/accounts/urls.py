from django.urls import path
from .views import * 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path("login/", CustomTokenObtainPairView.as_view(), name="login_view"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh_view"),
    path("register/", RegisterView.as_view(), name="create_user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('send-email-otp/', SendEmailOTPView.as_view(), name='send-email-otp'),
    path('verify-email-otp/', VerifyEmailOTPView.as_view(), name='verify-email-otp'),
]
