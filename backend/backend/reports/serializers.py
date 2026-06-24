from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "report_type", "parameters", "data", "created_at"]
        read_only_fields = fields


class GenerateReportSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=Report.ReportType.choices)
    patient_id = serializers.UUIDField(required=False)
    doctor_id = serializers.UUIDField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, attrs):
        report_type = attrs["report_type"]
        if report_type == Report.ReportType.PATIENT_HISTORY and not attrs.get("patient_id"):
            raise serializers.ValidationError({"patient_id": "Required for patient_history reports."})
        if report_type == Report.ReportType.DOCTOR_PERFORMANCE and not attrs.get("doctor_id"):
            raise serializers.ValidationError({"doctor_id": "Required for doctor_performance reports."})
        return attrs
