from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChatView, ChatSessionViewSet, SymptomEntryViewSet

app_name = "chatbot"

router = DefaultRouter()
router.register("sessions", ChatSessionViewSet, basename="chat-session")
router.register("symptoms", SymptomEntryViewSet, basename="symptom-entry")

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
] + router.urls
