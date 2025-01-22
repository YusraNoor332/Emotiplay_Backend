from googleapiclient.discovery import build
from django.conf import settings


def get_youtube_videos(query, max_results=5):
    youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet", q=query, maxResults=max_results, type="video"
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        video_data = {
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "video_id": item["id"]["videoId"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        }
        videos.append(video_data)

    return videos
