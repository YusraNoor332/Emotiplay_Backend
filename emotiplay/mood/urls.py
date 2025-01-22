from django.urls import path
from .views import MoodDetectionView, upload_image

urlpatterns = [
    path("", MoodDetectionView.as_view(), name="mood-detection"),
    path("upload", upload_image, name="mood-detection-by-image"),
]
