from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Validation
from .serializers import ValidationSerializer, ValidationCreateSerializer, ValidationFileSerializer
from .services.extractor import extract_rfc
from core.permissions import IsOwner
from core.exceptions import FileInvalid, ExtractionFailed

class ValidationListCreateView(generics.ListCreateAPIView):
    queryset = Validation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ValidationCreateSerializer
        return ValidationSerializer

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ValidationDetailView(generics.RetrieveAPIView):
    queryset = Validation.objects.all()
    serializer_class = ValidationSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class ValidationFileUploadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ValidationFileSerializer

    def post(self, request, pk):
        validation = get_object_or_404(Validation, pk=pk, created_by=request.user)

        if validation.status != "DRAFT":
            return Response(
                {"code": "INVALID_STATUS", "message": "Solo se puede subir archivo a validaciones en estado DRAFT"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]

        # Validaciones basicas de archivo
        if not uploaded_file.name.lower().endswith(".pdf"):
            raise FileInvalid(detail="Solo se permiten archivos .pdf")

        if uploaded_file.size > 5 * 1024 * 1024:  # 5 MB
            raise FileInvalid(detail="El archivo excede el tamano maximo permitido (5MB)")

        validation.file = uploaded_file
        validation.save()

        try:
            key, value = extract_rfc(validation.file.path)
            if key and value:
                validation.status = "PROCESSED"
                validation.extracted_key = key
                validation.extracted_value = value
            else:
                validation.status = "ERROR"
                validation.extracted_key = "RFC"
                raise ExtractionFailed()
        except Exception as e:
            validation.status = "ERROR"
            validation.save()
            raise ExtractionFailed(detail=str(e) or "No se pudo extraer el RFC del documento")

        validation.save()

        return Response({
            "validation_id": validation.id,
            "status": validation.status,
            "extracted_key": validation.extracted_key,
            "extracted_value": validation.extracted_value
        })
