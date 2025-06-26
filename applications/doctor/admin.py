from django.contrib import admin
from .models import Patient, Diagnosis
# Register your models here.
admin.site.register(Patient)
admin.site.register(Diagnosis)