from django_filters import rest_framework as filters
from .models import Appointment

class AppointmentFilter(filters.FilterSet):
    """
    Custom filter for Appointment
    """
    # Date range filters
    date_from = filters.DateTimeFilter(field_name='datetime', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='datetime', lookup_expr='lte')
    
    # Status filters
    status = filters.ChoiceFilter(choices=Appointment.STATUS_CHOICES)
    
    # Text search filters
    reason_contains = filters.CharFilter(field_name='reason', lookup_expr='icontains')
    notes_contains = filters.CharFilter(field_name='notes', lookup_expr='icontains')
    
    class Meta:
        model = Appointment
        fields = {
            'doctor': ['exact'],
            'patient': ['exact'],
            'status': ['exact'],
        } 