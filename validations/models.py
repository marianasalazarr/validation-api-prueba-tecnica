from django.db import models
from django.contrib.auth.models import User

class Validation(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('PROCESSED', 'Procesado'),
        ('ERROR', 'Error'),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    extracted_key = models.CharField(max_length=50, blank=True, null=True)
    extracted_value = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='validations/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validations')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.status}"
