from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Diagnosis(models.Model):
    """Model for storing diagnoses for users"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diagnoses')
    
    # Who/what created this diagnosis
    SOURCE_CHOICES = [
        ('ai', _('AI Assistant')),
        ('doctor', _('Human Doctor')),
        ('user', _('Self-Reported')),
        ('symptom_checker', _('Symptom Checker')),
    ]
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    
    # If doctor-provided, link to the doctor
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='doctor_diagnoses',
        limit_choices_to={'is_doctor': True}
    )
    
    # Diagnosis details
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Medical codes (optional)
    icd_code = models.CharField(max_length=20, blank=True, help_text=_("ICD-10 or ICD-11 code"))
    
    # Confidence level for AI diagnoses
    CONFIDENCE_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('confirmed', _('Confirmed')),
    ]
    confidence = models.CharField(max_length=20, choices=CONFIDENCE_CHOICES, default='medium')
    
    # Timestamps
    diagnosis_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('resolved', _('Resolved')),
        ('chronic', _('Chronic')),
        ('ruled_out', _('Ruled Out')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    resolved_date = models.DateField(null=True, blank=True)
    
    # Related data
    related_symptoms = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-diagnosis_date']
        verbose_name_plural = "Diagnoses"
    
    def __str__(self):
        return f"{self.title} - {self.get_source_display()} ({self.diagnosis_date})"

class Treatment(models.Model):
    """Model for treatment plans associated with diagnoses"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='treatments')
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='treatments')
    
    # Treatment details
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Treatment type
    TYPE_CHOICES = [
        ('medication', _('Medication')),
        ('procedure', _('Procedure')),
        ('therapy', _('Therapy')),
        ('lifestyle', _('Lifestyle Change')),
        ('monitoring', _('Monitoring')),
        ('other', _('Other')),
    ]
    treatment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Medication-specific fields
    medication_name = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    frequency = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('planned', _('Planned')),
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('discontinued', _('Discontinued')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Additional info
    instructions = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    
    # Progress tracking
    effectiveness_rating = models.PositiveIntegerField(null=True, blank=True, help_text=_("1-10 rating of effectiveness"))
    adherence_rating = models.PositiveIntegerField(null=True, blank=True, help_text=_("1-10 rating of adherence to treatment"))
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} for {self.diagnosis.title} ({self.get_status_display()})"

class FollowUp(models.Model):
    """Model for follow-up appointments related to diagnoses and treatments"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follow_ups')
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='follow_ups')
    treatments = models.ManyToManyField(Treatment, related_name='follow_ups', blank=True)
    
    # Follow-up details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Type of follow-up
    TYPE_CHOICES = [
        ('check_up', _('Check-up')),
        ('test', _('Medical Test')),
        ('specialist', _('Specialist Referral')),
        ('medication_review', _('Medication Review')),
        ('other', _('Other')),
    ]
    follow_up_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Timeline
    recommended_date = models.DateField()
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('recommended', _('Recommended')),
        ('scheduled', _('Scheduled')),
        ('completed', _('Completed')),
        ('missed', _('Missed')),
        ('cancelled', _('Cancelled')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recommended')
    
    # Results and notes
    results = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['recommended_date']
    
    def __str__(self):
        return f"{self.get_follow_up_type_display()} for {self.diagnosis.title} ({self.recommended_date})"
