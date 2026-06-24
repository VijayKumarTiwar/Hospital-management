from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalRecordViewSet

app_name = "patients"

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("medical-records", MedicalRecordViewSet, basename="medical-record")

urlpatterns = router.urls
