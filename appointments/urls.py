from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AppointmentViewSet, basename='appointments')

app_name = 'appointments'

urlpatterns = [
    path('', include(router.urls)),
] 