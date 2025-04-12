from django.db import models
from django.conf import settings

# Create your models here.

class ChatLog(models.Model):
    """Model for storing chat history with AI assistant"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_logs')
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"Chat with {self.user.email} at {self.timestamp}"
