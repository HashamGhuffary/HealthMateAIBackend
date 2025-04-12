from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    """Serializer for medical records"""
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = ['id', 'user', 'user_email', 'title', 'file', 'record_type', 
                  'record_type_display', 'description', 'uploaded_at']
        read_only_fields = ['id', 'user', 'user_email', 'uploaded_at']
        
    def create(self, validated_data):
        # Set the user to the current request user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 