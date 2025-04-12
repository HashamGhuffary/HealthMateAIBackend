from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):
    """Model for appointments between patients and doctors"""
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='appointments',
        limit_choices_to={'is_doctor': False}
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='doctor_appointments',
        limit_choices_to={'is_doctor': True}
    )
    datetime = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField(blank=True)
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
        ('completed', _('Completed')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    notes = models.TextField(blank=True, help_text=_("Doctor's notes about the appointment"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['datetime']
        
    def __str__(self):
        return f"Appointment: {self.patient} with Dr. {self.doctor.full_name or self.doctor.username} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"
        
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure end time is after start time
        if self.end_time <= self.datetime:
            raise ValidationError(_("End time must be after start time"))
            
        # Check for conflicting appointments
        conflicts = Appointment.objects.filter(
            models.Q(doctor=self.doctor) | models.Q(patient=self.patient),
            datetime__lt=self.end_time,
            end_time__gt=self.datetime,
            status__in=['pending', 'confirmed']
        ).exclude(id=self.id)
        
        if conflicts.exists():
            raise ValidationError(_("This time slot conflicts with another appointment"))
