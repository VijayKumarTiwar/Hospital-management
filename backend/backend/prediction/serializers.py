from rest_framework import serializers
from .models import PredictionRecord


class DiabetesInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=120)
    bmi = serializers.FloatField(min_value=10, max_value=70)
    glucose = serializers.FloatField(min_value=40, max_value=400)
    blood_pressure = serializers.FloatField(min_value=40, max_value=200)
    family_history = serializers.BooleanField()

    def to_model_input(self, validated_data):
        return {**validated_data, "family_history": int(validated_data["family_history"])}


class HeartDiseaseInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=120)
    cholesterol = serializers.FloatField(min_value=50, max_value=500)
    resting_bp = serializers.FloatField(min_value=60, max_value=250)
    max_heart_rate = serializers.FloatField(min_value=50, max_value=250)
    smoker = serializers.BooleanField()
    diabetic = serializers.BooleanField()

    def to_model_input(self, validated_data):
        return {
            **validated_data,
            "smoker": int(validated_data["smoker"]),
            "diabetic": int(validated_data["diabetic"]),
        }


class PredictionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRecord
        fields = [
            "id", "prediction_type", "input_data", "risk_score",
            "risk_label", "created_at",
        ]
        read_only_fields = fields
