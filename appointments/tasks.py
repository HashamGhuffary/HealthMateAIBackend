from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import datetime

@shared_task
def send_appointment_reminder():
    """Send email reminders for appointments scheduled in the next 24 hours"""
    from .models import Appointment
    
    # Get appointments scheduled in the next 24 hours
    now = timezone.now()
    tomorrow = now + datetime.timedelta(hours=24)
    
    upcoming_appointments = Appointment.objects.filter(
        datetime__range=(now, tomorrow),
        status='confirmed'
    )
    
    for appointment in upcoming_appointments:
        # Skip if no email is provided
        if not appointment.patient.email:
            continue
            
        # Format appointment time for display
        appointment_time = appointment.datetime.strftime('%B %d, %Y at %I:%M %p')
        doctor_name = appointment.doctor.full_name or appointment.doctor.username
        
        # Send email reminder
        subject = f'Reminder: Appointment with Dr. {doctor_name}'
        message = f"""
        Hello {appointment.patient.full_name or appointment.patient.username},
        
        This is a reminder that you have an appointment scheduled with Dr. {doctor_name} on {appointment_time}.
        
        If you need to reschedule, please do so at least 24 hours in advance.
        
        Thank you,
        HealthMateAI Team
        """
        
        # In production, use actual sender email
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@healthmateai.com')
        
        send_mail(
            subject,
            message,
            sender_email,
            [appointment.patient.email],
            fail_silently=True,
        )
        
    return f"Sent {upcoming_appointments.count()} appointment reminders"

@shared_task
def update_completed_appointments():
    """
    Automatically update status of appointments that have passed to 'completed'
    if they were previously 'confirmed'
    """
    from .models import Appointment
    
    now = timezone.now()
    
    # Get confirmed appointments that have ended
    completed_appointments = Appointment.objects.filter(
        end_time__lt=now,
        status='confirmed'
    )
    
    updated_count = completed_appointments.count()
    completed_appointments.update(status='completed')
    
    return f"Updated {updated_count} appointments to completed status" 