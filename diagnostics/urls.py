from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'diagnoses', views.DiagnosisViewSet, basename='diagnosis')
router.register(r'treatments', views.TreatmentViewSet, basename='treatment')
router.register(r'follow-ups', views.FollowUpViewSet, basename='follow-up')

urlpatterns = [
    path('', include(router.urls)),
] 