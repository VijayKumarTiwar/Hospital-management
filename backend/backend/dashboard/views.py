from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from prediction.models import PredictionRecord


class AdminDashboardView(APIView):
    """GET /api/dashboard/admin/ - system-wide stats for admins."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin_role:
            return Response({"detail": "Admin access required."}, status=403)

        today = timezone.now().date()
        last_30_days = timezone.now() - timedelta(days=30)

        data = {
            "total_patients": Patient.objects.count(),
            "total_doctors": Doctor.objects.count(),
            "appointments_today": Appointment.objects.filter(scheduled_at__date=today).count(),
            "appointments_by_status": dict(
                Appointment.objects.values("status").annotate(count=Count("id")).values_list("status", "count")
            ),
            "appointments_last_30_days": Appointment.objects.filter(created_at__gte=last_30_days).count(),
            "average_consultation_fee": Doctor.objects.aggregate(avg=Avg("consultation_fee"))["avg"],
            "high_risk_predictions_last_30_days": PredictionRecord.objects.filter(
                created_at__gte=last_30_days, risk_label="High"
            ).count(),
        }
        return Response(data)


class DoctorDashboardView(APIView):
    """GET /api/dashboard/doctor/ - personal stats for the logged-in doctor."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_doctor:
            return Response({"detail": "Doctor access required."}, status=403)

        doctor = request.user.doctor_profile
        today = timezone.now().date()

        appointments = Appointment.objects.filter(doctor=doctor)
        data = {
            "appointments_today": appointments.filter(scheduled_at__date=today).count(),
            "upcoming_appointments": appointments.filter(
                scheduled_at__gte=timezone.now(), status__in=["pending", "confirmed"]
            ).count(),
            "completed_appointments": appointments.filter(status="completed").count(),
            "cancelled_appointments": appointments.filter(status="cancelled").count(),
            "total_patients_seen": appointments.filter(status="completed").values("patient").distinct().count(),
            "average_rating": float(doctor.average_rating),
        }
        return Response(data)


class PatientDashboardView(APIView):
    """GET /api/dashboard/patient/ - personal stats for the logged-in patient."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_patient:
            return Response({"detail": "Patient access required."}, status=403)

        patient = request.user.patient_profile
        appointments = Appointment.objects.filter(patient=patient)

        data = {
            "upcoming_appointments": appointments.filter(
                scheduled_at__gte=timezone.now(), status__in=["pending", "confirmed"]
            ).count(),
            "past_appointments": appointments.filter(status="completed").count(),
            "total_medical_records": patient.medical_records.count(),
            "latest_predictions": list(
                PredictionRecord.objects.filter(user=request.user)
                .order_by("-created_at")[:5]
                .values("prediction_type", "risk_label", "risk_score", "created_at")
            ),
        }
        return Response(data)
