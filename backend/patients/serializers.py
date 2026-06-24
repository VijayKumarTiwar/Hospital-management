from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Patient, MedicalRecord


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bmi = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id", "user", "date_of_birth", "gender", "blood_group", "address",
            "emergency_contact_name", "emergency_contact_phone", "height_cm",
            "weight_kg", "bmi", "allergies", "chronic_conditions", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_bmi(self, obj):
        if obj.height_cm and obj.weight_kg:
            height_m = float(obj.height_cm) / 100
            return round(float(obj.weight_kg) / (height_m ** 2), 2)
        return None


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.user.get_full_name", read_only=True, default=None)

    class Meta:
        model = MedicalRecord
        fields = [
            "id", "patient", "doctor", "doctor_name", "diagnosis",
            "notes", "prescription", "attachment", "recorded_at",
        ]
        read_only_fields = ["id", "recorded_at"]
