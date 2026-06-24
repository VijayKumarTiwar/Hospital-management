from rest_framework import serializers
from django.utils import timezone
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.user.get_full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.get_full_name", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "patient", "patient_name", "doctor", "doctor_name",
            "scheduled_at", "duration_minutes", "status", "reason",
            "cancellation_reason", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_scheduled_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Cannot schedule an appointment in the past.")
        return value

    def validate(self, attrs):
        doctor = attrs.get("doctor") or getattr(self.instance, "doctor", None)
        scheduled_at = attrs.get("scheduled_at") or getattr(self.instance, "scheduled_at", None)
        qs = Appointment.objects.filter(
            doctor=doctor, scheduled_at=scheduled_at,
            status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This doctor already has an appointment at that time.")
        return attrs


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Used by patients to book; patient is auto-set from the request user."""

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "scheduled_at", "duration_minutes", "reason"]
        read_only_fields = ["id"]

    def validate_scheduled_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Cannot schedule an appointment in the past.")
        return value


class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status", "cancellation_reason"]

    def validate(self, attrs):
        if attrs.get("status") == Appointment.Status.CANCELLED and not attrs.get("cancellation_reason"):
            raise serializers.ValidationError({"cancellation_reason": "Required when cancelling."})
        return attrs
