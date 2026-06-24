from rest_framework import serializers
from .models import ChatSession, ChatMessage, SymptomEntry


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "text", "detected_urgency", "created_at"]
        read_only_fields = ["id", "created_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "created_at", "messages"]
        read_only_fields = ["id", "created_at"]


class ChatRequestSerializer(serializers.Serializer):
    """Input: a free-text message, optional existing session id."""

    message = serializers.CharField(max_length=2000)
    session_id = serializers.UUIDField(required=False, allow_null=True)


class SymptomEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomEntry
        fields = ["id", "keyword", "advice", "urgency", "suggested_specialization"]
