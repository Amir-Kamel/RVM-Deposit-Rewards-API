from rest_framework import serializers
import re
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = [
            'username', 'email', 'password', 'phone',
            'address', 'gender', 'age',
            'first_name', 'last_name'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_username(self, value):
        value = value.strip()
        if not re.match(r'^[a-zA-Z_ ]+$', value):
            raise serializers.ValidationError("Only letters, underscores, and spaces are allowed in username.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError("Invalid email format")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', value):
            raise serializers.ValidationError("Password must be at least 8 characters long and include both letters and numbers")
        return value

    def validate_phone(self, value):
        if not re.match(r'^(010|012|015|011)\d{8}$', value):
            raise serializers.ValidationError("Phone number must be 11 digits and start with 010, 012, 015, or 011")
        return value

    def validate_first_name(self, value):
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("Last name must contain only letters.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data.get("phone"),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            address=validated_data.get("address", ""),
            gender=validated_data.get("gender"),
            age=validated_data.get("age"),
        )

    