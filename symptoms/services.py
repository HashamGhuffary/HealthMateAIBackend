import json
import logging
from django.conf import settings
import openai

logger = logging.getLogger(__name__)

def analyze_symptoms(symptom_check):
    """
    Analyze a user's symptoms using OpenAI API and update the symptom check object.
    
    Args:
        symptom_check: A SymptomCheck instance
    """
    try:
        # Format symptom information for OpenAI
        user = symptom_check.user
        symptoms_data = []
        print("symptom_check", symptom_check)
        
        for user_symptom in symptom_check.symptoms.all():
            symptom_info = {
                "name": user_symptom.symptom.name,
                "severity": user_symptom.get_severity_display(),
                "duration": f"Since {user_symptom.onset_date.strftime('%Y-%m-%d')}",
                "notes": user_symptom.notes
            }
            symptoms_data.append(symptom_info)
        
        # Get additional user data
        user_info = {
            "age": user.age,
            "gender": user.get_gender_display() if hasattr(user, 'get_gender_display') else user.gender,
            "additional_info": symptom_check.additional_info
        }
        
        # Create prompt for OpenAI
        system_prompt = """
        You are a medical assistant AI. Analyze the following symptoms and provide:
        1. A brief analysis of the symptoms
        2. A list of possible conditions with confidence levels (low, medium, high)
        3. Recommendations for the patient
        4. Whether this requires emergency attention (true/false)
        
        Format your response as a JSON object with these keys:
        {
            "analysis": "Your detailed analysis here",
            "possible_conditions": [
                {"condition": "Condition name", "confidence": "low/medium/high", "match_percentage": 0-100, "description": "Brief description"}
            ],
            "recommendations": "Your recommendations here",
            "emergency": true/false
        }
        """
        
        # Create the user prompt with all symptom information
        user_prompt = f"""
        Patient Information:
        - Age: {user_info['age']}
        - Gender: {user_info['gender']}
        - Additional Info: {json.dumps(user_info['additional_info'])}
        
        Symptoms:
        {json.dumps(symptoms_data, indent=2)}
        
        Please analyze these symptoms and provide an assessment.
        """
        print("user_prompt", user_prompt)
        
        # Query OpenAI API
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",  # Use appropriate model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature for more deterministic results
        )
        
        # Extract response
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        result = json.loads(result_text)
        
        # Update the symptom check with analysis results
        symptom_check.ai_analysis = result["analysis"]
        symptom_check.possible_conditions = result["possible_conditions"]
        symptom_check.recommendations = result["recommendations"]
        symptom_check.emergency_level = result["emergency"]
        symptom_check.save()
        
    except Exception as e:
        logger.error(f"Error in symptom analysis: {str(e)}")
        # Set a fallback analysis
        symptom_check.ai_analysis = "Unable to complete symptom analysis. Please consult with a healthcare professional."
        symptom_check.possible_conditions = []
        symptom_check.recommendations = "Please consult with a healthcare professional for a proper diagnosis."
        symptom_check.emergency_level = False
        symptom_check.save() 