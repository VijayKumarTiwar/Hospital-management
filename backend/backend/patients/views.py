from rest_framework import viewsets, permissions
from accounts.permissions import IsPatient, IsOwnerOrAdmin
from .models import Patient, MedicalRecord
from .serializers import PatientSerializer, MedicalRecordSerializer


class IsSelfOrDoctorOrAdmin(permissions.BasePermission):
    """Patients can manage only their own profile; doctors/admins can view any."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin_role or request.user.is_doctor:
            return True
        return obj.user == request.user


class PatientViewSet(viewsets.ModelViewSet):
    """
    /api/patients/        - admins/doctors see all, patients see only themselves
    /api/patients/{id}/   - retrieve/update own profile
    """

    serializer_class = PatientSerializer
    permission_classes = [IsSelfOrDoctorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_role or user.is_doctor:
            return Patient.objects.select_related("user").all()
        return Patient.objects.select_related("user").filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """
    /api/patients/medical-records/  - doctors create records, patients view their own.
    """

    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_role:
            return MedicalRecord.objects.all()
        if user.is_doctor:
            return MedicalRecord.objects.filter(doctor__user=user)
        return MedicalRecord.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        doctor = getattr(user, "doctor_profile", None)
        serializer.save(doctor=doctor)
