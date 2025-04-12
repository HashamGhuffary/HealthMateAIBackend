from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from users.permissions import IsOwnerOrReadOnly
from .filters import MedicalRecordFilter

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicalRecordFilter
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']
    
    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return MedicalRecord.objects.none()
            
        user = self.request.user
        # Mainly for future use and development
        if user.is_doctor:
            # Doctors can see all medical records
            return MedicalRecord.objects.all()
        else:
            # Patients can see their own records
            return MedicalRecord.objects.filter(user=user)
