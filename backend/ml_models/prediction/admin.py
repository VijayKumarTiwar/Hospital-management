from django.contrib import admin
from .models import PredictionRecord

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ["user", "prediction_type", "risk_score", "risk_label", "created_at"]
    list_filter = ["prediction_type", "risk_label"]
