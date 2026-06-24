from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsDoctor, IsAdminRole
from .models import Doctor, Specialization, DoctorAvailability
from .serializers import (
    DoctorSerializer, DoctorListSerializer, SpecializationSerializer,
    DoctorAvailabilitySerializer,
)


class IsDoctorOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_admin_role)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin_role or obj.user == request.user


class DoctorViewSet(viewsets.ModelViewSet):
    """
    /api/doctors/            - list/search all doctors
    /api/doctors/{id}/       - retrieve/update/delete (owner or admin)
    /api/doctors/{id}/availability/ - nested availability management
    """

    queryset = Doctor.objects.select_related("user").prefetch_related("specializations", "availabilities")
    permission_classes = [IsDoctorOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_available", "specializations"]
    search_fields = ["user__first_name", "user__last_name", "specializations__name"]
    ordering_fields = ["consultation_fee", "years_of_experience", "average_rating"]

    def get_serializer_class(self):
        if self.action == "list":
            return DoctorListSerializer
        return DoctorSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return DoctorAvailability.objects.filter(doctor__user=self.request.user)

    def perform_create(self, serializer):
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)
