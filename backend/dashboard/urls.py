from django.urls import path
from .views import AdminDashboardView, DoctorDashboardView, PatientDashboardView

app_name = "dashboard"

urlpatterns = [
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("doctor/", DoctorDashboardView.as_view(), name="doctor-dashboard"),
    path("patient/", PatientDashboardView.as_view(), name="patient-dashboard"),
]
