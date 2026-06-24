import uuid
from django.conf import settings
from django.db import models


class Report(models.Model):
    class ReportType(models.TextChoices):
        PATIENT_HISTORY = "patient_history", "Patient Visit History"
        DOCTOR_PERFORMANCE = "doctor_performance", "Doctor Performance"
        APPOINTMENT_SUMMARY = "appointment_summary", "Appointment Summary"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    report_type = models.CharField(max_length=25, choices=ReportType.choices)
    parameters = models.JSONField(default=dict, blank=True, help_text="Filters used to generate this report")
    data = models.JSONField(help_text="The computed report payload")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_report_type_display()} by {self.generated_by} @ {self.created_at}"
