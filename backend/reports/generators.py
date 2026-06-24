"""
Pure functions that compute report payloads. Kept separate from views so
they're easy to unit test or reuse (e.g. from a Celery task or management
command) without going through HTTP.
"""

from django.db.models import Count, Avg, Q
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor


def generate_patient_history_report(patient_id):
    patient = Patient.objects.select_related("user").get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).select_related("doctor__user")

    return {
        "patient_id": str(patient.id),
        "patient_name": patient.user.get_full_name(),
        "total_appointments": appointments.count(),
        "completed": appointments.filter(status="completed").count(),
        "cancelled": appointments.filter(status="cancelled").count(),
        "no_show": appointments.filter(status="no_show").count(),
        "medical_records_count": patient.medical_records.count(),
        "visits": [
            {
                "doctor": a.doctor.user.get_full_name(),
                "scheduled_at": a.scheduled_at.isoformat(),
                "status": a.status,
                "reason": a.reason,
            }
            for a in appointments.order_by("-scheduled_at")[:50]
        ],
    }


def generate_doctor_performance_report(doctor_id):
    doctor = Doctor.objects.select_related("user").get(id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    total = appointments.count()
    completed = appointments.filter(status="completed").count()

    return {
        "doctor_id": str(doctor.id),
        "doctor_name": doctor.user.get_full_name(),
        "total_appointments": total,
        "completed": completed,
        "cancelled": appointments.filter(status="cancelled").count(),
        "no_show": appointments.filter(status="no_show").count(),
        "completion_rate": round(completed / total, 3) if total else 0,
        "average_rating": float(doctor.average_rating),
        "unique_patients": appointments.values("patient").distinct().count(),
    }


def generate_appointment_summary_report(start_date=None, end_date=None):
    qs = Appointment.objects.all()
    if start_date:
        qs = qs.filter(scheduled_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(scheduled_at__date__lte=end_date)

    by_status = dict(qs.values("status").annotate(count=Count("id")).values_list("status", "count"))

    return {
        "start_date": str(start_date) if start_date else None,
        "end_date": str(end_date) if end_date else None,
        "total_appointments": qs.count(),
        "by_status": by_status,
        "busiest_doctors": list(
            qs.values("doctor__user__first_name", "doctor__user__last_name")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        ),
    }
