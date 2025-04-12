import openai
from django.conf import settings
from .models import ChatLog

# Initialize the OpenAI client with the API key
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
# client = openai.OpenAI()

def get_user_chat_history(user, limit=5):

    chat_logs = ChatLog.objects.filter(user=user).order_by('-timestamp')[:limit]
    
    # Format history for OpenAI context
    history = []
    for log in reversed(chat_logs):
        history.append({"role": "user", "content": log.message})
        history.append({"role": "assistant", "content": log.response})
        
    return history

def query_openai(message, history=None):

    if not settings.OPENAI_API_KEY:
        return "API key not configured. Please set the OPENAI_API_KEY environment variable."
    

    messages = [
        {"role": "system", "content": "You are a supportive health assistant. Give correct, useful information regarding health issues but don't provide final medical diagnoses. Always remind users to consult healthcare professionals for individual medical advice. Refuse to answer completely any questions or inquiries that have no relation to healthcare"}
    ]
    

        
    # Add the current message
    messages.append({"role": "user", "content": message})
    
    try:
        # Make API call to OpenAI using the client
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Using a cost-effective model
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        # Extract and return the response text
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error querying OpenAI: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def log_chat(user, message, response):
    ChatLog.objects.create(
        user=user,
        message=message,
        response=response
    ) 