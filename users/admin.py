from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'full_name', 'is_doctor', 'is_staff')
    search_fields = ('email', 'username', 'full_name')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'age', 'gender', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doctor',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_doctor'),
        }),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
