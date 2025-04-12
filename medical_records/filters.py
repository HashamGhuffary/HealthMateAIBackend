from django_filters import rest_framework as filters
from .models import MedicalRecord

class MedicalRecordFilter(filters.FilterSet):
    """
    Custom filter for MedicalRecord
    """
    # Date range filters
    uploaded_after = filters.DateTimeFilter(field_name='uploaded_at', lookup_expr='gte')
    uploaded_before = filters.DateTimeFilter(field_name='uploaded_at', lookup_expr='lte')
    
    # Text search filters
    title_contains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description_contains = filters.CharFilter(field_name='description', lookup_expr='icontains')
    
    class Meta:
        model = MedicalRecord
        fields = {
            'record_type': ['exact'],
            'user': ['exact'],
        } 