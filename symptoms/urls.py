from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'predefined', views.SymptomViewSet, basename='symptom')
router.register(r'user-symptoms', views.UserSymptomViewSet, basename='user-symptom')
router.register(r'checks', views.SymptomCheckViewSet, basename='symptom-check')

urlpatterns = [
    path('', include(router.urls)),
] 