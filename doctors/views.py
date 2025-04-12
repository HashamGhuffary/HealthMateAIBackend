from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DoctorProfile, DoctorReview
from .serializers import DoctorProfileSerializer, DoctorReviewSerializer, DoctorProfileUpdateSerializer
from users.permissions import IsDoctor, IsPatient
from .filters import DoctorProfileFilter

# Create your views here.

class DoctorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving doctor profiles.
    """
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DoctorProfileFilter
    search_fields = ['user__full_name', 'bio']
    
    def get_queryset(self):
        # Skip queryset filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return DoctorProfile.objects.none()
        return DoctorProfile.objects.all()


class DoctorProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    View for updating a doctor's own profile.
    """
    serializer_class = DoctorProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_object(self):
        # Skip queryset filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return None
        return self.request.user.doctor_profile


class DoctorReviewCreateView(generics.CreateAPIView):
    """
    View for creating a review for a doctor.
    """
    serializer_class = DoctorReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['doctor_id'] = self.kwargs.get('doctor_id')
        return context
        
    def perform_create(self, serializer):
        doctor_id = self.kwargs.get('doctor_id')
        doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
        serializer.save(patient=self.request.user, doctor=doctor_profile)


class DoctorReviewListView(generics.ListAPIView):
    """
    View for listing reviews for a specific doctor.
    """
    serializer_class = DoctorReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Skip queryset filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return DoctorReview.objects.none()
        doctor_id = self.kwargs.get('doctor_id')
        return DoctorReview.objects.filter(doctor_id=doctor_id)
