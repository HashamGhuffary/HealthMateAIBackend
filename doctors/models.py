from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class DoctorProfile(models.Model):
    """Model for doctor profiles with additional information"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialties = models.JSONField(default=list, help_text="List of doctor's specialties")
    bio = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    location = models.CharField(max_length=255, blank=True)
    available_times = models.JSONField(default=dict, help_text="Dictionary of available time slots")
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    
    def __str__(self):
        return f"Dr. {self.user.full_name or self.user.username}"
    
    class Meta:
        ordering = ['-rating']


class DoctorReview(models.Model):
    """Model for storing reviews for doctors"""
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='reviews')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('doctor', 'patient')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.doctor} by {self.patient.username}"
    
    def save(self, *args, **kwargs):
        # Save the review
        super().save(*args, **kwargs)
        
        # Update the doctor's rating
        reviews = DoctorReview.objects.filter(doctor=self.doctor)
        if reviews:
            self.doctor.rating = sum(r.rating for r in reviews) / reviews.count()
            self.doctor.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_doctor_profile(sender, instance, created, **kwargs):
    """Create a DoctorProfile when a new doctor user is created"""
    if created and instance.is_doctor:
        DoctorProfile.objects.create(user=instance)
