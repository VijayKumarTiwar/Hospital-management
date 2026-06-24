from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatSession, ChatMessage, SymptomEntry
from .serializers import (
    ChatSessionSerializer, ChatRequestSerializer, SymptomEntrySerializer,
)
from .engine import get_response


class ChatView(APIView):
    """
    POST /api/chatbot/chat/
    body: {"message": "I have a fever and headache", "session_id": "<uuid, optional>"}

    Creates a new ChatSession if session_id is omitted, logs both the user
    message and bot reply, and returns the bot's response.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id")

        if session_id:
            session = ChatSession.objects.filter(id=session_id, user=request.user).first()
            if not session:
                return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            session = ChatSession.objects.create(user=request.user)

        ChatMessage.objects.create(session=session, sender=ChatMessage.Sender.USER, text=message)

        bot_result = get_response(message)

        bot_message = ChatMessage.objects.create(
            session=session,
            sender=ChatMessage.Sender.BOT,
            text=bot_result["reply"],
            detected_urgency=bot_result["urgency"],
        )

        return Response(
            {
                "session_id": session.id,
                "reply": bot_result["reply"],
                "urgency": bot_result["urgency"],
                "matched_keywords": bot_result["matched_keywords"],
                "suggested_specialization": bot_result["suggested_specialization"],
                "message_id": bot_message.id,
            },
            status=status.HTTP_200_OK,
        )


class ChatSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """/api/chatbot/sessions/ - view past chat history for the current user."""

    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).prefetch_related("messages")


class SymptomEntryViewSet(viewsets.ModelViewSet):
    """/api/chatbot/symptoms/ - admin-managed knowledge base."""

    queryset = SymptomEntry.objects.all()
    serializer_class = SymptomEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
