from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Symptom, UserSymptom, SymptomCheck
from .serializers import (
    SymptomSerializer, 
    UserSymptomSerializer, 
    UserSymptomCreateSerializer,
    SymptomCheckSerializer,
    SymptomCheckCreateSerializer
)
from .services import analyze_symptoms

class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving predefined symptoms.
    """
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description', 'body_part']
    filterset_fields = ['body_part']

class UserSymptomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user symptoms.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['symptom', 'severity', 'is_active']
    ordering_fields = ['created_at', 'onset_date', 'severity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return UserSymptom.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserSymptomCreateSerializer
        return UserSymptomSerializer
    
    @action(detail=False, methods=['get'])
    def active(self):
        """Get only active symptoms"""
        active_symptoms = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_symptoms, many=True)
        return Response(serializer.data)

class SymptomCheckViewSet(viewsets.ModelViewSet):
    """
    API endpoint for symptom checking sessions.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SymptomCheck.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SymptomCheckCreateSerializer
        return SymptomCheckSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        symptom_check = serializer.save()
        
        # Process with AI analysis
        analyze_symptoms(symptom_check)
        
        # Return the full symptom check with analysis
        result_serializer = SymptomCheckSerializer(symptom_check)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get most recent symptom check"""
        recent_check = self.get_queryset().first()
        if not recent_check:
            return Response({"detail": "No symptom checks found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SymptomCheckSerializer(recent_check)
        return Response(serializer.data)
