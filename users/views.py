from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import CustomUser
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class RegistrationAPIView(APIView):
    """
    API view for user registration.
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Create a new user account and return authentication tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password', 'password_confirmation'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password (min 8 characters)'),
                'password_confirmation': openapi.Schema(type=openapi.TYPE_STRING, description='Password confirmation'),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s full name'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='User\'s age'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s gender (M/F/O/N)'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s location'),
                'is_doctor': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether user is a doctor'),
            }
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                                'location': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_doctor': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        ),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(description="Bad request", schema=openapi.Schema(type=openapi.TYPE_OBJECT))
        }
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            # Create response data
            response_data = {
                'user': UserProfileSerializer(user).data,
                'tokens': tokens
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    API view for user login.
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Login with email and password to receive authentication tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                                'location': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_doctor': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        ),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(description="Invalid credentials", schema=openapi.Schema(type=openapi.TYPE_OBJECT))
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            # Create response data
            response_data = {
                'user': UserProfileSerializer(user).data,
                'tokens': tokens
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    API view for refreshing access tokens.
    """
    @swagger_auto_schema(
        operation_description="Use refresh token to get a new access token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Token refresh successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='New access token'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='New refresh token (if ROTATE_REFRESH_TOKENS=True)'),
                    }
                )
            ),
            401: openapi.Response(description="Invalid refresh token", schema=openapi.Schema(type=openapi.TYPE_OBJECT))
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get current user profile information",
        responses={
            200: openapi.Response(
                description="User profile retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'location': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_doctor': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
            401: openapi.Response(description="Authentication credentials not provided")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_description="Update current user profile information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s full name'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='User\'s age'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s gender (M/F/O/N)'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s location'),
            }
        ),
        responses={
            200: openapi.Response(
                description="User profile updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'location': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_doctor': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
            400: openapi.Response(description="Bad request"),
            401: openapi.Response(description="Authentication credentials not provided")
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_description="Partially update current user profile information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s full name'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='User\'s age'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s gender (M/F/O/N)'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s location'),
            }
        ),
        responses={
            200: openapi.Response(
                description="User profile updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'location': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_doctor': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
            400: openapi.Response(description="Bad request"),
            401: openapi.Response(description="Authentication credentials not provided")
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user
