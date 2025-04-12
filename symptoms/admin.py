from django.contrib import admin
from .models import Symptom, UserSymptom, SymptomCheck

admin.site.register(Symptom)
admin.site.register(UserSymptom)
admin.site.register(SymptomCheck)

