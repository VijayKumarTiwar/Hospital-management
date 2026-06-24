from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Report
from .serializers import ReportSerializer, GenerateReportSerializer
from .generators import (
    generate_patient_history_report,
    generate_doctor_performance_report,
    generate_appointment_summary_report,
)


class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_admin_role)


class GenerateReportView(APIView):
    """
    POST /api/reports/generate/
    body examples:
      {"report_type": "patient_history", "patient_id": "<uuid>"}
      {"report_type": "doctor_performance", "doctor_id": "<uuid>"}
      {"report_type": "appointment_summary", "start_date": "2026-01-01", "end_date": "2026-06-01"}
    """

    permission_classes = [IsDoctorOrAdmin]

    def post(self, request):
        serializer = GenerateReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        report_type = params["report_type"]

        if report_type == Report.ReportType.PATIENT_HISTORY:
            data = generate_patient_history_report(params["patient_id"])
        elif report_type == Report.ReportType.DOCTOR_PERFORMANCE:
            data = generate_doctor_performance_report(params["doctor_id"])
        else:
            data = generate_appointment_summary_report(
                params.get("start_date"), params.get("end_date")
            )

        report = Report.objects.create(
            generated_by=request.user,
            report_type=report_type,
            parameters={k: str(v) for k, v in params.items() if k != "report_type"},
            data=data,
        )
        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """/api/reports/reports/ - view previously generated reports."""

    serializer_class = ReportSerializer
    permission_classes = [IsDoctorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = Report.objects.all()
        if user.is_admin_role:
            return qs
        return qs.filter(generated_by=user)
