from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="HealthMateAI API",
        default_version='v1',
        description="API for HealthMateAI application",
        terms_of_service="https://www.healthmateai.com/terms/",
        contact=openapi.Contact(email="hasham@healthmateai.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URLs
api_urlpatterns = [
    path('auth/', include('users.urls')),
    path('records/', include('medical_records.urls')),
    path('chat/', include('ai_assistant.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    
    # New modules
    path('symptoms/', include('symptoms.urls')),
    path('diagnostics/', include('diagnostics.urls')),
    
]

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(api_urlpatterns)),
    
    # API documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
