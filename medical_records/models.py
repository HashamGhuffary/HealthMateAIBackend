from django.db import models
from django.conf import settings

class MedicalRecord(models.Model):
    """Model for storing medical records and files"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='records/')
    RECORD_TYPES = [
        ('lab', 'Lab Report'), 
        ('prescription', 'Prescription'),
        ('imaging', 'Imaging'),
        ('discharge', 'Discharge Summary'),
        ('other', 'Other')
    ]
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_record_type_display()})"
