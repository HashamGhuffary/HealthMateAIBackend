from rest_framework import serializers
from .models import ChatLog

class ChatLogSerializer(serializers.ModelSerializer):
    """Serializer for chat logs"""
    
    class Meta:
        model = ChatLog
        fields = ['id', 'message', 'response', 'timestamp']
        read_only_fields = fields 