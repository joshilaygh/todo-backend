from rest_framework import serializers
from .models import Todo
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        # Ensure that the email is unique
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already taken.")
        return value

    def validate_password(self, value):
        # Ensure the password is strong enough (add more checks if necessary)
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        # Ensure that the user is being created with email, username, and password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields='__all__'