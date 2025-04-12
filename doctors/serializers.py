from rest_framework import serializers
from .models import DoctorProfile, DoctorReview
from users.serializers import UserProfileSerializer

class DoctorReviewSerializer(serializers.ModelSerializer):
    """Serializer for doctor reviews"""
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = DoctorReview
        fields = ['id', 'doctor', 'patient', 'patient_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'doctor', 'patient', 'patient_name', 'created_at']


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for doctor profiles"""
    user = UserProfileSerializer(read_only=True)
    reviews = DoctorReviewSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialties', 'bio', 'education', 'experience_years', 
                  'rating', 'location', 'available_times', 'profile_picture', 
                  'reviews', 'review_count']
        read_only_fields = ['id', 'user', 'rating', 'reviews']
        
    def get_review_count(self, obj):
        return obj.reviews.count()


class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating doctor profiles"""
    
    class Meta:
        model = DoctorProfile
        fields = ['specialties', 'bio', 'education', 'experience_years', 
                  'location', 'available_times', 'profile_picture'] 