from django.urls import path
from .views import VideoRecommendationView, AIVideoRecommendationView

urlpatterns = [
    path("", AIVideoRecommendationView.as_view(), name="AIVideoRecommendationView"),
    path("recommend/", VideoRecommendationView.as_view(), name="video-recommendation"),
]
