from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Symptom(models.Model):
    """Model for predefined symptoms that users can select or AI can identify"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    body_part = models.CharField(max_length=50, blank=True)
    severity_scale = models.PositiveIntegerField(default=1, help_text="Scale of 1-10 for typical severity")
    common_related_conditions = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return self.name

class UserSymptom(models.Model):
    """Model for tracking a user's specific symptom instance"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='symptoms')
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, related_name='user_instances')
    
    SEVERITY_CHOICES = [
        (1, _('Very Mild')),
        (2, _('Mild')),
        (3, _('Moderate')),
        (4, _('Uncomfortable')),
        (5, _('Concerning')),
        (6, _('Severe')),
        (7, _('Very Severe')),
        (8, _('Extreme')),
        (9, _('Unbearable')),
        (10, _('Emergency')),
    ]
    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES)
    
    onset_date = models.DateField()
    is_active = models.BooleanField(default=True, help_text="Whether the symptom is still present")
    resolved_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.symptom.name} (Severity: {self.severity})"

class SymptomCheck(models.Model):
    """Model for symptom checking sessions with results"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='symptom_checks')
    symptoms = models.ManyToManyField(UserSymptom, related_name='check_sessions')
    
    # Additional questions and responses
    additional_info = models.JSONField(default=dict, blank=True, 
                                     help_text="Structured additional information like age, gender, medical history")
    
    # Analysis and results 
    ai_analysis = models.TextField(blank=True)
    possible_conditions = models.JSONField(default=list, blank=True,
                                         help_text="List of possible conditions with confidence levels")
    
    recommendations = models.TextField(blank=True)
    emergency_level = models.BooleanField(default=False, help_text="Whether this requires emergency attention")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Symptom Check"
        verbose_name_plural = "Symptom Checks"
    
    def __str__(self):
        return f"Symptom Check for {self.user.full_name} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
