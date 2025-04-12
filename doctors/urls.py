from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.DoctorProfileViewSet, basename='doctors')

app_name = 'doctors'

urlpatterns = [
    path('profile/', views.DoctorProfileUpdateView.as_view(), name='profile'),
    path('<int:doctor_id>/reviews/', views.DoctorReviewListView.as_view(), name='reviews'),
    path('<int:doctor_id>/reviews/create/', views.DoctorReviewCreateView.as_view(), name='create-review'),
    path('', include(router.urls)),
] 