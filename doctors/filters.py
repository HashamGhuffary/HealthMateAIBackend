from django_filters import rest_framework as filters
from .models import DoctorProfile

class DoctorProfileFilter(filters.FilterSet):
    """
    Custom filter for DoctorProfile that handles JSONField filtering
    """
    # Filter for specialties (JSONField)
    specialty = filters.CharFilter(method='filter_specialty')
    
    # Regular filters
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    
    class Meta:
        model = DoctorProfile
        fields = ['rating_min', 'rating_max', 'location', 'specialty']
        
    def filter_specialty(self, queryset, name, value):
        """
        Custom filter method for specialty field (JSONField)
        Filters doctors that have the specified specialty in their specialties list
        """
        # This requires PostgreSQL with JSONField containment operator @>
        # For SQLite, we can use a simple string contains check
        return queryset.filter(specialties__contains=value) 