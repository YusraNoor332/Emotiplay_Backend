from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from deepface import DeepFace
import cv2
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import time


class MoodDetectionView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get("image")

        if not file:
            return Response(
                {"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Convert uploaded image file to OpenCV format
        np_img = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        try:
            # Analyze the image using DeepFace
            result = DeepFace.analyze(img, actions=["emotion"])
            mood = result[0].get("dominant_emotion", "Mood Not Found")
            return Response({"mood": mood}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES:
        image = request.FILES["image"]
        if not image:
            return JsonResponse({"error": "No image provided."}, status=400)

        timestamp = int(time.time())  # Current timestamp in seconds
        file_name = f"selfie_{timestamp}.png"  # Filename with timestamp

        image_content = image.read()

        # file_path = default_storage.save(
        #     f"uploads/{file_name}", ContentFile(image_content)
        # )

        np_img = np.frombuffer(image_content, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        try:
            # Save the image with a relative path under the 'uploads' directory
            result = DeepFace.analyze(img, actions=["emotion"])
            mood = result[0].get("dominant_emotion", "Mood Not Found")
            return JsonResponse(
                {
                    "message": "Image uploaded successfully",
                    # "file_path": f"/media/{file_path}",
                    "mood": mood,
                }
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Error analyzing emotion: {str(e)}"}, status=406
            )
    return JsonResponse({"error": "No image file found"}, status=400)
