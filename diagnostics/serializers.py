from rest_framework import serializers
from .models import Diagnosis, Treatment, FollowUp
from users.serializers import UserProfileSerializer

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = [
            'id', 'user', 'diagnosis', 'title', 'description',
            'treatment_type', 'medication_name', 'dosage', 'frequency', 'duration',
            'start_date', 'end_date', 'status', 'instructions',
            'side_effects', 'precautions', 'effectiveness_rating',
            'adherence_rating', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Treatment.objects.create(user=user, **validated_data)

class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = [
            'id', 'user', 'diagnosis', 'treatments', 'title', 'description',
            'follow_up_type', 'recommended_date', 'scheduled_date', 'completed_date',
            'status', 'results', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        treatments = validated_data.pop('treatments', [])
        follow_up = FollowUp.objects.create(user=user, **validated_data)
        
        if treatments:
            follow_up.treatments.set(treatments)
        
        return follow_up

class DiagnosisSerializer(serializers.ModelSerializer):
    treatments = TreatmentSerializer(many=True, read_only=True)
    follow_ups = FollowUpSerializer(many=True, read_only=True)
    doctor_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Diagnosis
        fields = [
            'id', 'user', 'source', 'doctor', 'doctor_details',
            'title', 'description', 'icd_code', 'confidence',
            'diagnosis_date', 'created_at', 'updated_at',
            'status', 'resolved_date', 'related_symptoms',
            'notes', 'treatments', 'follow_ups'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_doctor_details(self, obj):
        if obj.doctor:
            return {
                'name': obj.doctor.full_name,
                'email': obj.doctor.email,
                'specialty': obj.doctor.doctor_profile.specialties[0] if hasattr(obj.doctor, 'doctor_profile') and obj.doctor.doctor_profile.specialties else None
            }
        return None
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Diagnosis.objects.create(user=user, **validated_data)

class DiagnosisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = [
            'source', 'doctor', 'title', 'description',
            'icd_code', 'confidence', 'diagnosis_date',
            'status', 'resolved_date', 'related_symptoms', 'notes'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Diagnosis.objects.create(user=user, **validated_data)

class DiagnosisUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = [
            'title', 'description', 'icd_code', 'confidence',
            'status', 'resolved_date', 'notes'
        ]

class TreatmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = [
            'title', 'description', 'status', 'end_date',
            'effectiveness_rating', 'adherence_rating', 'notes'
        ]

class FollowUpUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = [
            'title', 'description', 'scheduled_date', 
            'completed_date', 'status', 'results', 'notes'
        ] 