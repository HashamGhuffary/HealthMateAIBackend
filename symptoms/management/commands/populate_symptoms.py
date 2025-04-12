from django.core.management.base import BaseCommand
from symptoms.models import Symptom

class Command(BaseCommand):
    help = 'Populates the database with predefined symptoms'

    def handle(self, *args, **kwargs):
        symptoms_data = [
            {
                'name': 'Headache',
                'description': 'Pain in the head or upper neck area',
                'body_part': 'Head',
                'severity_scale': 5,
                'common_related_conditions': ['Migraine', 'Tension Headache', 'Sinusitis']
            },
            {
                'name': 'Fever',
                'description': 'Elevated body temperature above normal range',
                'body_part': 'Whole Body',
                'severity_scale': 6,
                'common_related_conditions': ['Influenza', 'Common Cold', 'COVID-19']
            },
            {
                'name': 'Cough',
                'description': 'Sudden expulsion of air from the lungs',
                'body_part': 'Chest',
                'severity_scale': 4,
                'common_related_conditions': ['Bronchitis', 'Common Cold', 'Asthma']
            },
            {
                'name': 'Chest Pain',
                'description': 'Pain or discomfort in the chest area',
                'body_part': 'Chest',
                'severity_scale': 8,
                'common_related_conditions': ['Angina', 'Heart Attack', 'Pleurisy']
            },
            {
                'name': 'Shortness of Breath',
                'description': 'Difficulty breathing or feeling breathless',
                'body_part': 'Chest',
                'severity_scale': 7,
                'common_related_conditions': ['Asthma', 'Pneumonia', 'Heart Failure']
            },
            {
                'name': 'Abdominal Pain',
                'description': 'Pain in the stomach or abdominal area',
                'body_part': 'Abdomen',
                'severity_scale': 6,
                'common_related_conditions': ['Gastritis', 'Appendicitis', 'Irritable Bowel Syndrome']
            },
            {
                'name': 'Nausea',
                'description': 'Feeling of sickness with an inclination to vomit',
                'body_part': 'Stomach',
                'severity_scale': 5,
                'common_related_conditions': ['Food Poisoning', 'Migraine', 'Motion Sickness']
            },
            {
                'name': 'Dizziness',
                'description': 'Feeling of lightheadedness or unsteadiness',
                'body_part': 'Head',
                'severity_scale': 5,
                'common_related_conditions': ['Vertigo', 'Low Blood Pressure', 'Dehydration']
            },
            {
                'name': 'Fatigue',
                'description': 'Extreme tiredness or lack of energy',
                'body_part': 'Whole Body',
                'severity_scale': 4,
                'common_related_conditions': ['Anemia', 'Chronic Fatigue Syndrome', 'Depression']
            },
            {
                'name': 'Joint Pain',
                'description': 'Pain or discomfort in the joints',
                'body_part': 'Joints',
                'severity_scale': 5,
                'common_related_conditions': ['Arthritis', 'Rheumatoid Arthritis', 'Gout']
            },
            {
                'name': 'Muscle Pain',
                'description': 'Pain or discomfort in the muscles',
                'body_part': 'Muscles',
                'severity_scale': 4,
                'common_related_conditions': ['Fibromyalgia', 'Muscle Strain', 'Influenza']
            },
            {
                'name': 'Rash',
                'description': 'Change in skin texture or color',
                'body_part': 'Skin',
                'severity_scale': 4,
                'common_related_conditions': ['Allergic Reaction', 'Eczema', 'Psoriasis']
            },
            {
                'name': 'Sore Throat',
                'description': 'Pain or irritation in the throat',
                'body_part': 'Throat',
                'severity_scale': 4,
                'common_related_conditions': ['Strep Throat', 'Common Cold', 'Tonsillitis']
            },
            {
                'name': 'Runny Nose',
                'description': 'Excessive nasal discharge',
                'body_part': 'Nose',
                'severity_scale': 3,
                'common_related_conditions': ['Common Cold', 'Allergies', 'Sinusitis']
            },
            {
                'name': 'Back Pain',
                'description': 'Pain in the back area',
                'body_part': 'Back',
                'severity_scale': 6,
                'common_related_conditions': ['Muscle Strain', 'Herniated Disc', 'Sciatica']
            },
            {
                'name': 'Insomnia',
                'description': 'Difficulty falling or staying asleep',
                'body_part': 'Whole Body',
                'severity_scale': 5,
                'common_related_conditions': ['Anxiety', 'Depression', 'Sleep Apnea']
            },
            {
                'name': 'Anxiety',
                'description': 'Feeling of worry, nervousness, or unease',
                'body_part': 'Whole Body',
                'severity_scale': 6,
                'common_related_conditions': ['Generalized Anxiety Disorder', 'Panic Disorder', 'Depression']
            },
            {
                'name': 'Diarrhea',
                'description': 'Frequent loose or watery bowel movements',
                'body_part': 'Abdomen',
                'severity_scale': 5,
                'common_related_conditions': ['Food Poisoning', 'Irritable Bowel Syndrome', 'Gastroenteritis']
            },
            {
                'name': 'Constipation',
                'description': 'Difficulty in passing stools',
                'body_part': 'Abdomen',
                'severity_scale': 4,
                'common_related_conditions': ['Irritable Bowel Syndrome', 'Dehydration', 'Hypothyroidism']
            },
            {
                'name': 'Blurred Vision',
                'description': 'Lack of sharpness of vision',
                'body_part': 'Eyes',
                'severity_scale': 6,
                'common_related_conditions': ['Migraine', 'Diabetes', 'Glaucoma']
            }
        ]

        created_count = 0
        for symptom_data in symptoms_data:
            symptom, created = Symptom.objects.get_or_create(
                name=symptom_data['name'],
                defaults=symptom_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created symptom: {symptom.name}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new symptoms')) 