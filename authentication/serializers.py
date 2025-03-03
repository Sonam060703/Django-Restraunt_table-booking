# authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from pydantic import BaseModel, EmailStr, validator, Field
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

# Pydantic model for user registration validation
class UserRegistrationSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_validation(cls, v):
        try:
            validate_password(v)
        except ValidationError as e:
            raise ValueError(str(e))
        return v

# DRF Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        # Using Pydantic for validation
        UserRegistrationSchema(**data)
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_admin', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')