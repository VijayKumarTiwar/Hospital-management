from django.contrib import admin
from .models import Patient, MedicalRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["user", "gender", "blood_group", "date_of_birth"]
    search_fields = ["user__first_name", "user__last_name"]


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "diagnosis", "recorded_at"]
    list_filter = ["recorded_at"]
