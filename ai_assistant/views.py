from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .models import ChatLog
from .services import query_openai, get_user_chat_history, log_chat
from .serializers import ChatLogSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_ai(request):
    """
    API endpoint for chatting with the AI assistant.
    
    Request body should contain a 'message' field with the user's message.
    Returns the AI assistant's response.
    """
    message = request.data.get('message')
    if not message:
        return Response(
            {"error": "Please provide a message"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # Get chat history for context
    history = get_user_chat_history(request.user)
    
    # Query OpenAI API
    ai_response = query_openai(message, history)
    print("ai_response", ai_response)
    
    # Log the conversation
    log_chat(request.user, message, ai_response)
    
    return Response({"reply": ai_response})


class ChatHistoryListView(generics.ListAPIView):
    """
    API endpoint for listing a user's chat history.
    """
    serializer_class = ChatLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Skip queryset filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return ChatLog.objects.none()
        return ChatLog.objects.filter(user=self.request.user).order_by('timestamp')
