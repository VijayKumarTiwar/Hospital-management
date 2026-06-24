from rest_framework import serializers
from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    appointment_time = serializers.DateTimeField(source="appointment.scheduled_at", read_only=True)
    patient_name = serializers.CharField(source="appointment.patient.user.get_full_name", read_only=True)
    doctor_name = serializers.CharField(source="appointment.doctor.user.get_full_name", read_only=True)

    class Meta:
        model = Reminder
        fields = [
            "id", "appointment", "appointment_time", "patient_name", "doctor_name",
            "remind_at", "status", "message", "sent_at", "created_at",
        ]
        read_only_fields = ["id", "sent_at", "created_at"]
