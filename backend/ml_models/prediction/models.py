import uuid
from django.conf import settings
from django.db import models


class PredictionRecord(models.Model):
    """Stores the inputs/outputs of every risk prediction made, for audit and history."""

    class PredictionType(models.TextChoices):
        DIABETES = "diabetes", "Diabetes Risk"
        HEART_DISEASE = "heart_disease", "Heart Disease Risk"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="predictions")
    prediction_type = models.CharField(max_length=20, choices=PredictionType.choices)
    input_data = models.JSONField()
    risk_score = models.FloatField(help_text="Probability between 0 and 1")
    risk_label = models.CharField(max_length=20, help_text="e.g. Low / Moderate / High")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.prediction_type} - {self.risk_label}"
