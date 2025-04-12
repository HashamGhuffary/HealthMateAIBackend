from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Diagnosis, Treatment, FollowUp
from .serializers import (
    DiagnosisSerializer,
    DiagnosisCreateSerializer,
    DiagnosisUpdateSerializer,
    TreatmentSerializer,
    TreatmentUpdateSerializer,
    FollowUpSerializer,
    FollowUpUpdateSerializer
)
from symptoms.models import SymptomCheck
from .services import generate_treatment_plan

class DiagnosisViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing diagnoses.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source', 'status', 'confidence']
    ordering_fields = ['diagnosis_date', 'created_at']
    ordering = ['-diagnosis_date']
    
    def get_queryset(self):
        return Diagnosis.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DiagnosisCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DiagnosisUpdateSerializer
        return DiagnosisSerializer
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark a diagnosis as resolved"""
        diagnosis = self.get_object()
        diagnosis.status = 'resolved'
        diagnosis.resolved_date = timezone.now().date()
        diagnosis.save()
        
        serializer = DiagnosisSerializer(diagnosis)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_chronic(self, request, pk=None):
        """Mark a diagnosis as chronic"""
        diagnosis = self.get_object()
        diagnosis.status = 'chronic'
        diagnosis.save()
        
        serializer = DiagnosisSerializer(diagnosis)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generate_treatment(self, request, pk=None):
        """Generate a treatment plan for this diagnosis"""
        diagnosis = self.get_object()
        
        # Generate treatment plan
        treatment = generate_treatment_plan(diagnosis)
        
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def from_symptom_check(self, request):
        """Create a diagnosis from a symptom check result"""
        symptom_check_id = request.data.get('symptom_check_id')
        if not symptom_check_id:
            return Response(
                {"error": "symptom_check_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            symptom_check = SymptomCheck.objects.get(id=symptom_check_id, user=request.user)
            
            # Get most likely condition
            conditions = symptom_check.possible_conditions
            if not conditions:
                return Response(
                    {"error": "No conditions found in symptom check"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Sort by confidence and get highest
            top_condition = sorted(
                conditions, 
                key=lambda x: {'low': 0, 'medium': 1, 'high': 2}.get(x.get('confidence', 'low'), 0),
                reverse=True
            )[0]
            
            # Create diagnosis
            diagnosis = Diagnosis.objects.create(
                user=request.user,
                source='symptom_checker',
                title=top_condition.get('condition', 'Unknown Condition'),
                description=top_condition.get('description', ''),
                confidence=top_condition.get('confidence', 'low'),
                diagnosis_date=timezone.now().date(),
                status='active',
                related_symptoms=[s.symptom.name for s in symptom_check.symptoms.all()]
            )
            
            serializer = DiagnosisSerializer(diagnosis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except SymptomCheck.DoesNotExist:
            return Response(
                {"error": "Symptom check not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class TreatmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing treatments.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['diagnosis', 'treatment_type', 'status']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']
    
    def get_queryset(self):
        return Treatment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TreatmentUpdateSerializer
        return TreatmentSerializer
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a treatment as completed"""
        treatment = self.get_object()
        treatment.status = 'completed'
        treatment.end_date = timezone.now().date()
        treatment.save()
        
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def discontinue(self, request, pk=None):
        """Mark a treatment as discontinued"""
        treatment = self.get_object()
        treatment.status = 'discontinued'
        treatment.end_date = timezone.now().date()
        treatment.save()
        
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate the effectiveness and adherence of a treatment"""
        treatment = self.get_object()
        
        effectiveness = request.data.get('effectiveness')
        adherence = request.data.get('adherence')
        
        if effectiveness is not None:
            treatment.effectiveness_rating = int(effectiveness)
        
        if adherence is not None:
            treatment.adherence_rating = int(adherence)
        
        treatment.save()
        
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)

class FollowUpViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing follow-ups.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['diagnosis', 'follow_up_type', 'status']
    ordering_fields = ['recommended_date', 'scheduled_date']
    ordering = ['recommended_date']
    
    def get_queryset(self):
        return FollowUp.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return FollowUpUpdateSerializer
        return FollowUpSerializer
    
    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        """Schedule a follow-up"""
        follow_up = self.get_object()
        
        scheduled_date = request.data.get('scheduled_date')
        if not scheduled_date:
            return Response(
                {"error": "scheduled_date is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow_up.scheduled_date = scheduled_date
        follow_up.status = 'scheduled'
        follow_up.save()
        
        serializer = FollowUpSerializer(follow_up)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a follow-up as completed"""
        follow_up = self.get_object()
        
        results = request.data.get('results', '')
        
        follow_up.status = 'completed'
        follow_up.completed_date = timezone.now().date()
        follow_up.results = results
        follow_up.save()
        
        serializer = FollowUpSerializer(follow_up)
        return Response(serializer.data)
