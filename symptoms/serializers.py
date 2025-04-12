from rest_framework import serializers
from .models import Symptom, UserSymptom, SymptomCheck
from users.serializers import UserProfileSerializer
from django.utils import timezone

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

class UserSymptomSerializer(serializers.ModelSerializer):
    symptom_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSymptom
        fields = [
            'id', 'user', 'symptom', 'symptom_name', 'severity', 
            'onset_date', 'is_active', 'resolved_date', 'notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_symptom_name(self, obj):
        return obj.symptom.name if obj.symptom else None

class UserSymptomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSymptom
        fields = [
            'symptom', 'severity', 'onset_date', 
            'is_active', 'resolved_date', 'notes'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return UserSymptom.objects.create(user=user, **validated_data)

class SymptomCheckSerializer(serializers.ModelSerializer):
    symptoms = UserSymptomSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = SymptomCheck
        fields = [
            'id', 'user', 'user_details', 'symptoms', 'additional_info',
            'ai_analysis', 'possible_conditions', 'recommendations',
            'emergency_level', 'created_at'
        ]
        read_only_fields = ['ai_analysis', 'possible_conditions', 'recommendations', 'emergency_level', 'created_at']
    
    def get_user_details(self, obj):
        return {
            'name': obj.user.full_name,
            'email': obj.user.email,
            'age': obj.user.age,
            'gender': obj.user.gender
        }

class SymptomCheckCreateSerializer(serializers.ModelSerializer):
    symptom_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = SymptomCheck
        fields = ['symptom_ids', 'additional_info']
    
    def create(self, validated_data):
        user = self.context['request'].user
        symptom_ids = validated_data.pop('symptom_ids', [])
        additional_info = validated_data.get('additional_info', {})
        
        # Extract severity data from additional_info
        severity_data = additional_info.get('severity', [])
        
        # Create symptom check
        symptom_check = SymptomCheck.objects.create(user=user, **validated_data)
        
        # Create UserSymptom instances
        for symptom_id in symptom_ids:
            # Find matching severity data for this symptom
            symptom_severity = next(
                (item for item in severity_data if item.get('symptom_id') == symptom_id),
                {'severity': 5}  # Default severity if not specified
            )
            
            # Create UserSymptom
            user_symptom = UserSymptom.objects.create(
                user=user,
                symptom_id=symptom_id,
                severity=symptom_severity.get('severity', 5),
                onset_date=timezone.now().date(),
                is_active=True
            )
            
            # Add to symptom check
            symptom_check.symptoms.add(user_symptom)
        
        return symptom_check 