from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Reminder
from .serializers import ReminderSerializer
from .services import send_due_reminders


class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_admin_role)


class ReminderViewSet(viewsets.ModelViewSet):
    """
    /api/reminders/                  - doctors/admins manage reminders
    /api/reminders/dispatch-due/     - manually trigger sending of due reminders
    """

    serializer_class = ReminderSerializer
    permission_classes = [IsDoctorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = Reminder.objects.select_related("appointment__patient__user", "appointment__doctor__user")
        if user.is_admin_role:
            return qs
        return qs.filter(appointment__doctor__user=user)

    @action(detail=False, methods=["post"], url_path="dispatch-due")
    def dispatch_due(self, request):
        count = send_due_reminders()
        return Response({"sent": count}, status=status.HTTP_200_OK)
