import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"
        NO_SHOW = "no_show", "No Show"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        "doctors.Doctor", on_delete=models.CASCADE, related_name="appointments"
    )
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    reason = models.TextField(blank=True, help_text="Reason for visit / chief complaint")
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_at"]
        indexes = [
            models.Index(fields=["doctor", "scheduled_at"]),
            models.Index(fields=["patient", "scheduled_at"]),
        ]

    def __str__(self):
        return f"{self.patient} with {self.doctor} @ {self.scheduled_at}"

    def clean(self):
        # Prevent double-booking the same doctor at the same time slot.
        overlapping = Appointment.objects.filter(
            doctor=self.doctor,
            scheduled_at=self.scheduled_at,
            status__in=[self.Status.PENDING, self.Status.CONFIRMED],
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This doctor already has an appointment at that time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
