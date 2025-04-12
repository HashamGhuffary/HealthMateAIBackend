import json
import logging
from django.conf import settings
from django.utils import timezone
import openai
from .models import Treatment

logger = logging.getLogger(__name__)

def generate_treatment_plan(diagnosis):
    """
    Generate a treatment plan for a diagnosis using AI.
    
    Args:
        diagnosis: The Diagnosis instance
    
    Returns:
        Treatment instance with AI-generated treatment plan
    """
    try:
        # Get user and diagnosis info
        user = diagnosis.user
        
        # Use OpenAI to generate a treatment plan
        treatment_data = get_ai_treatment_recommendation(diagnosis)
        
        # Create treatment object
        treatment = Treatment.objects.create(
            user=user,
            diagnosis=diagnosis,
            title=treatment_data['title'],
            description=treatment_data['description'],
            treatment_type=treatment_data['type'],
            medication_name=treatment_data.get('medication_name', ''),
            dosage=treatment_data.get('dosage', ''),
            frequency=treatment_data.get('frequency', ''),
            duration=treatment_data.get('duration', ''),
            start_date=timezone.now().date(),
            status='planned',
            instructions=treatment_data.get('instructions', ''),
            side_effects=treatment_data.get('side_effects', ''),
            precautions=treatment_data.get('precautions', '')
        )
        
        return treatment
        
    except Exception as e:
        logger.error(f"Error generating treatment plan: {str(e)}")
        # Create a basic treatment as fallback
        return Treatment.objects.create(
            user=diagnosis.user,
            diagnosis=diagnosis,
            title=f"Treatment plan for {diagnosis.title}",
            description="Please consult with a healthcare professional for a proper treatment plan.",
            treatment_type='other',
            start_date=timezone.now().date(),
            status='planned'
        )

def get_ai_treatment_recommendation(diagnosis):
    """
    Use OpenAI to generate a treatment recommendation.
    
    Args:
        diagnosis: The Diagnosis instance
    
    Returns:
        Dictionary with treatment information
    """
    try:
        # Format diagnosis information for AI
        diagnosis_data = {
            'title': diagnosis.title,
            'description': diagnosis.description,
            'icd_code': diagnosis.icd_code,
            'status': diagnosis.status,
            'related_symptoms': diagnosis.related_symptoms,
            'user_age': diagnosis.user.age if diagnosis.user.age else "Unknown",
            'user_gender': diagnosis.user.gender if diagnosis.user.gender else "Unknown"
        }
        
        # Create system prompt
        system_prompt = """
        You are a medical treatment recommendation AI. Based on the diagnosis information provided, 
        suggest an appropriate treatment plan. Consider the condition, patient demographics, and symptoms.
        
        Format your response as a JSON object with these keys:
        {
            "title": "Brief treatment plan title",
            "description": "Detailed description of the treatment approach",
            "type": "One of: medication, procedure, therapy, lifestyle, monitoring, other",
            "medication_name": "Name of medication (if applicable)",
            "dosage": "Recommended dosage (if applicable)",
            "frequency": "How often to take/do (if applicable)",
            "duration": "How long to continue treatment",
            "instructions": "Detailed instructions for following the treatment",
            "side_effects": "Potential side effects to watch for",
            "precautions": "Precautions and warnings"
        }
        
        IMPORTANT: Begin with general treatment approaches. DO NOT prescribe specific medications with specific dosages, 
        as this requires a doctor's supervision. Instead, mention classes of medications that might be appropriate and
        general dosing considerations. Always recommend consulting with a healthcare professional.
        """
        
        # Create the user prompt with diagnosis data
        user_prompt = f"""
        Diagnosis Information:
        {json.dumps(diagnosis_data, indent=2)}
        
        Please suggest an appropriate treatment plan for this diagnosis.
        """
        
        # Query OpenAI API
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",  # Use appropriate model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,  # Conservative for medical advice
        )
        
        # Extract and parse response
        result_text = response.choices[0].message.content.strip()
        result = json.loads(result_text)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in AI treatment recommendation: {str(e)}")
        # Return a fallback treatment plan
        return {
            "title": "General management approach",
            "description": "This is a general management approach. Please consult with a healthcare professional for a personalized treatment plan.",
            "type": "other",
            "instructions": "Consult with a healthcare professional for proper diagnosis and treatment."
        } 