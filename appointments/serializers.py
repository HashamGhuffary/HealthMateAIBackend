from rest_framework import serializers
from .models import Appointment
from users.serializers import UserProfileSerializer
from django.utils.translation import gettext_lazy as _

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for appointments"""
    patient_details = UserProfileSerializer(source='patient', read_only=True)
    doctor_details = UserProfileSerializer(source='doctor', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'patient_details', 'doctor_details', 
                  'datetime', 'end_time', 'reason', 'status', 'status_display', 
                  'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status_display', 'created_at', 'updated_at']
        
    def validate(self, data):
        # Validate appointment conflicts
        datetime = data.get('datetime')
        end_time = data.get('end_time')
        doctor = data.get('doctor')
        patient = data.get('patient')
        
        # If this is an update, get the existing instance
        instance = self.instance
        
        if datetime and end_time:
            if end_time <= datetime:
                raise serializers.ValidationError({"end_time": _("End time must be after start time")})
                
            # Check for conflicting appointments
            from django.db.models import Q
            
            conflicts_query = Q(
                Q(doctor=doctor) | Q(patient=patient),
                datetime__lt=end_time,
                end_time__gt=datetime,
                status__in=['pending', 'confirmed']
            )
            
            # Exclude the current instance if we're updating
            if instance:
                conflicts = Appointment.objects.filter(conflicts_query).exclude(id=instance.id)
            else:
                conflicts = Appointment.objects.filter(conflicts_query)
                
            if conflicts.exists():
                raise serializers.ValidationError({"datetime": _("This time slot conflicts with another appointment")})
                
        return data
        
    def create(self, validated_data):
        # Set the patient to the current request user if not specified
        if 'patient' not in validated_data:
            validated_data['patient'] = self.context['request'].user
            
        return super().create(validated_data) 