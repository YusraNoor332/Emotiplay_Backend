from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .youtube_service import get_youtube_videos
from django.conf import settings
import requests
from .helper import invoke_model
import re
import random


class VideoRecommendationView(APIView):
    def post(self, request, *args, **kwargs):
        mood = request.data.get("mood", "")

        if not mood:
            return Response(
                {"error": "Mood is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch videos based on the mood
        videos = get_youtube_videos(mood)
        return Response({"mood": mood, "videos": videos}, status=status.HTTP_200_OK)


class AIVideoRecommendationView(APIView):
    def post(self, request, *args, **kwargs):

        mood = request.data.get("mood")
        max_count = request.data.get("max_count", "")
        print(max_count)

        if not mood:
            return Response(
                {"error": "Mood not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            keywords = self.generate_key_words(mood)
            videos = self.get_youtube_videos(
                keywords, max_results=int(max_count) if max_count else 10
            )

            return Response({"videos": videos}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def generate_key_words(self, mood):
        prompt = f"""
        You are tasked with generating mood-specific non-conflicting music-related keywords for music recommendations.
        The user's mood is '{mood}', and they live in Pakistan.
        Provide keywords tailored to this mood and location.The singers should be from both hollywood and bollywood For example:
        - For 'happy': 'celebration', 'Bollywood', 'desi beats', 'Neha Kakkar', 'Arijit Singh', 'katy perry'
        - For 'sad': 'slow', 'acoustic', 'melancholy'
        And these keywords should always be random 
        Format the response as >>> Keywords:'keyword1', 'keyword2', 'keyword3', ...
        """
        # prompt = f"Generate a list of music-related keywords for a '{mood}' mood in Pakistan. Ensure the keywords are specific to music genres only. Format: >>> Keywords:'keyword1', 'keyword2', ..."
        # prompt = f"Generate only and only keywords nothing else and the whole response should be composed in this format >>> Keywords:'keyword1', 'keyword2','keyword3',...  that I can search over the youtube to get videos for some person with mood: '{mood}' and thatperson lives in Pakistan."
        response = invoke_model(prompt)

        match = re.search(r"Keywords:(.*)", response)
        if match:
            keywords = match.group(1).strip()  # Get the text after "Keywords:"
            keywords_list = [
                keyword.strip(" '") for keyword in keywords.split(",")
            ]  # Parse into a list
            # print("Extracted Keywords:", keywords_list)
            return keywords_list
        else:
            print("No keywords found in the response.")
            return []

    def get_youtube_videos(self, keywords: list, max_results: int = 10):
        """Search for YouTube videos using the YouTube Data API based on the keywords"""
        youtube_search_url = "https://www.googleapis.com/youtube/v3/search"
        selected_keywords = (
            random.sample(keywords, 3) if len(keywords) > 3 else keywords
        )
        print("Selected Keywords for Query:", selected_keywords)
        params = {
            "part": "snippet",
            "q": "+".join(selected_keywords),
            "key": settings.YOUTUBE_API_KEY,
            "maxResults": max_results,
            "type": "video",
            "safeSearch": "strict",
            "regionCode": "PK",
            "videoCategoryId": "10",  # Music
        }

        response = requests.get(youtube_search_url, params=params)
        if response.status_code == 200:
            print(response.text)
            items = response.json().get("items", [])
            videos = [
                {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "video_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "thumbnail": (
                        item["snippet"]["thumbnails"]["high"][
                            "url"
                        ]  # Extract high-quality thumbnail
                        if "high" in item["snippet"]["thumbnails"]
                        else item["snippet"]["thumbnails"]["default"]["url"]
                    ),  # Fallback to default thumbnail
                }
                for item in items
                if item["id"]["kind"] == "youtube#video"
            ]
            return videos
        else:
            raise Exception(f"Failed to fetch videos from YouTube API: {response.text}")
