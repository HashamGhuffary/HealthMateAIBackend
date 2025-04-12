from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    password_confirmation = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password_confirmation', 'full_name', 'age', 'gender', 'location', 'is_doctor']
    
    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password_confirmation')
        
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")
            
        return data
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
        

class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
                
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
                
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'full_name', 'age', 'gender', 'location', 'is_doctor']
        read_only_fields = ['id', 'email', 'is_doctor'] 