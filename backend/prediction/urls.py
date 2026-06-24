from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DiabetesRiskView, HeartDiseaseRiskView, PredictionHistoryViewSet

app_name = "prediction"

router = DefaultRouter()
router.register("history", PredictionHistoryViewSet, basename="prediction-history")

urlpatterns = [
    path("diabetes/", DiabetesRiskView.as_view(), name="diabetes-risk"),
    path("heart-disease/", HeartDiseaseRiskView.as_view(), name="heart-disease-risk"),
] + router.urls
