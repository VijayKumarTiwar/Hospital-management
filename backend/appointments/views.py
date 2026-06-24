from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import (
    AppointmentSerializer, AppointmentCreateSerializer, AppointmentStatusUpdateSerializer,
)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    /api/appointments/                 - list (scoped to role) / create (patients book)
    /api/appointments/{id}/            - retrieve/update/delete
    /api/appointments/{id}/set-status/ - PATCH to confirm/cancel/complete
    """

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "doctor", "patient"]

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.select_related("patient__user", "doctor__user")
        if user.is_admin_role:
            return qs
        if user.is_doctor:
            return qs.filter(doctor__user=user)
        return qs.filter(patient__user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        if self.action == "set_status":
            return AppointmentStatusUpdateSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        patient = self.request.user.patient_profile
        serializer.save(patient=patient)

    @action(detail=True, methods=["patch"], url_path="set-status")
    def set_status(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)
