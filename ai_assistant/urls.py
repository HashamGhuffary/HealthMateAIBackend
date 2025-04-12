from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('chat/', views.chat_with_ai, name='chat'),
    path('history/', views.ChatHistoryListView.as_view(), name='history'),
] 