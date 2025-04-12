from django.contrib import admin
from .models import DoctorProfile, DoctorReview

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'location', 'experience_years')
    search_fields = ('user__email', 'user__username', 'user__full_name', 'bio')
    list_filter = ('rating', 'location')
    readonly_fields = ('rating',)

@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    search_fields = ('doctor__user__username', 'patient__username', 'comment')
    list_filter = ('rating', 'created_at')
