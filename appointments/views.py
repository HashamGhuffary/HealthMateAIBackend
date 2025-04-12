from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer
from users.permissions import IsDoctor, IsPatient, IsOwnerOrReadOnly
from .filters import AppointmentFilter

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for appointments.
    
    Provides CRUD operations for appointments.
    Includes filters for date, status, and doctor/patient.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AppointmentFilter
    search_fields = ['reason', 'notes']
    ordering_fields = ['datetime', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """
        Filter appointments based on user role.
        Doctors see appointments where they are the doctor.
        Patients see appointments where they are the patient.
        """
        # Skip queryset filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Appointment.objects.none()
            
        user = self.request.user
        
        if user.is_doctor:
            return Appointment.objects.filter(doctor=user)
        else:
            return Appointment.objects.filter(patient=user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsDoctor])
    def update_status(self, request, pk=None):
        """
        Update the status of an appointment.
        Only doctors can update appointment status.
        """
        appointment = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {"error": "Please provide a status"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if new_status not in [choice[0] for choice in Appointment.STATUS_CHOICES]:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        appointment.status = new_status
        appointment.save()
        
        return Response(AppointmentSerializer(appointment).data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsDoctor])
    def add_notes(self, request, pk=None):
        """
        Add notes to an appointment.
        Only doctors can add notes.
        """
        appointment = self.get_object()
        notes = request.data.get('notes', '')
        
        appointment.notes = notes
        appointment.save()
        
        return Response(AppointmentSerializer(appointment).data)
