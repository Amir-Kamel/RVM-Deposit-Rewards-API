from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # your custom user model

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_verified', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Email Verification', {'fields': ('is_verified', 'email_otp', 'email_otp_created_at')}),
    )





