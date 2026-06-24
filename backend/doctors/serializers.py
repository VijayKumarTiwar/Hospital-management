from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Doctor, Specialization, DoctorAvailability


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "name", "description"]


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source="get_weekday_display", read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = ["id", "weekday", "weekday_display", "start_time", "end_time"]


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)
    specialization_ids = serializers.PrimaryKeyRelatedField(
        queryset=Specialization.objects.all(), many=True, write_only=True,
        source="specializations", required=False,
    )
    availabilities = DoctorAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id", "user", "specializations", "specialization_ids",
            "license_number", "years_of_experience", "consultation_fee",
            "bio", "is_available", "average_rating", "availabilities", "created_at",
        ]
        read_only_fields = ["id", "average_rating", "created_at"]


class DoctorListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing/searching doctors."""

    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    specializations = serializers.StringRelatedField(many=True)

    class Meta:
        model = Doctor
        fields = [
            "id", "full_name", "specializations", "years_of_experience",
            "consultation_fee", "is_available", "average_rating",
        ]
