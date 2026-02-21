from django.urls import path
from .views import ValidationListCreateView, ValidationDetailView, ValidationFileUploadView

urlpatterns = [
    path('', ValidationListCreateView.as_view(), name='validation-list-create'),
    path('<int:pk>/', ValidationDetailView.as_view(), name='validation-detail'),
    path('<int:pk>/file/', ValidationFileUploadView.as_view(), name='validation-file-upload'),
]
