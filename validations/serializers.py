from rest_framework import serializers
from .models import Validation

class ValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['id', 'title', 'status', 'extracted_key', 'extracted_value', 'created_at']
        read_only_fields = ['status', 'extracted_key', 'extracted_value', 'created_at']

class ValidationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['title']

class ValidationFileSerializer(serializers.Serializer):
    file = serializers.FileField()
