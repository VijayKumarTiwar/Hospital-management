import uuid
from django.conf import settings
from django.db import models


class SymptomEntry(models.Model):
    """Knowledge base: keyword -> advice mapping used by the rule-based chatbot."""

    class Urgency(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High - seek care soon"
        EMERGENCY = "emergency", "Emergency - seek immediate care"

    keyword = models.CharField(max_length=100, unique=True, help_text="e.g. 'fever', 'chest pain'")
    advice = models.TextField()
    urgency = models.CharField(max_length=10, choices=Urgency.choices, default=Urgency.LOW)
    suggested_specialization = models.ForeignKey(
        "doctors.Specialization", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["keyword"]

    def __str__(self):
        return self.keyword


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_sessions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Session {self.id} - {self.user}"


class ChatMessage(models.Model):
    class Sender(models.TextChoices):
        USER = "user", "User"
        BOT = "bot", "Bot"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=4, choices=Sender.choices)
    text = models.TextField()
    detected_urgency = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.sender}] {self.text[:50]}"
