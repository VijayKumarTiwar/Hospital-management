import uuid
from django.db import models


class Reminder(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        SENT = "sent", "Sent"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(
        "appointments.Appointment", on_delete=models.CASCADE, related_name="reminders"
    )
    remind_at = models.DateTimeField(help_text="When this reminder should be sent")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)
    message = models.CharField(max_length=255, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["remind_at"]

    def __str__(self):
        return f"Reminder for {self.appointment} at {self.remind_at}"
