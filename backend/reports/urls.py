from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GenerateReportView, ReportViewSet

app_name = "reports"

router = DefaultRouter()
router.register("reports", ReportViewSet, basename="report")

urlpatterns = [
    path("generate/", GenerateReportView.as_view(), name="generate-report"),
] + router.urls
