from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecializationViewSet, DoctorAvailabilityViewSet

app_name = "doctors"

router = DefaultRouter()
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("specializations", SpecializationViewSet, basename="specialization")
router.register("availability", DoctorAvailabilityViewSet, basename="availability")

urlpatterns = router.urls
