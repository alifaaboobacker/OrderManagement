from datetime import datetime
from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import re


def validate_password_strength(value):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Password must be at least 8 characters long, contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character (@$!%*?&)."
        )
    return value


def validate_contact_number(value):
    if not re.match(r'^\+?1?\d{9,15}$', str(value)):
        raise serializers.ValidationError("Enter a valid phone number.")
    return value


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, validators=[validate_password_strength])
    contact_number = serializers.CharField(validators=[validate_contact_number])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'contact_number', 'role', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True}
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_role(self, value):
        valid_roles = dict(User.ROLE_CHOICES).keys()
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role '{value}' is not valid.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            contact_number=validated_data.get('contact_number'),
            role=validated_data.get('role')
        )
        return user