from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PredictionRecord
from .serializers import (
    DiabetesInputSerializer, HeartDiseaseInputSerializer, PredictionRecordSerializer,
)
from .ml import predict_diabetes, predict_heart_disease


class DiabetesRiskView(APIView):
    """POST /api/prediction/diabetes/ - predicts diabetes risk from clinical inputs."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DiabetesInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_input = serializer.to_model_input(serializer.validated_data)

        result = predict_diabetes(model_input)

        record = PredictionRecord.objects.create(
            user=request.user,
            prediction_type=PredictionRecord.PredictionType.DIABETES,
            input_data=serializer.validated_data,
            risk_score=result["risk_score"],
            risk_label=result["risk_label"],
        )
        return Response(PredictionRecordSerializer(record).data, status=status.HTTP_200_OK)


class HeartDiseaseRiskView(APIView):
    """POST /api/prediction/heart-disease/ - predicts heart disease risk."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = HeartDiseaseInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_input = serializer.to_model_input(serializer.validated_data)

        result = predict_heart_disease(model_input)

        record = PredictionRecord.objects.create(
            user=request.user,
            prediction_type=PredictionRecord.PredictionType.HEART_DISEASE,
            input_data=serializer.validated_data,
            risk_score=result["risk_score"],
            risk_label=result["risk_label"],
        )
        return Response(PredictionRecordSerializer(record).data, status=status.HTTP_200_OK)


class PredictionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """/api/prediction/history/ - past predictions for the current user."""

    serializer_class = PredictionRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PredictionRecord.objects.filter(user=self.request.user)
