# your_app/management/commands/add_youtube_categories.py

from django.core.management.base import BaseCommand

print("Running add_youtube_categories")
from video.models import Category

YOUTUBE_CATEGORIES = [
    {"category_id": 1, "name": "Film & Animation"},
    {"category_id": 2, "name": "Autos & Vehicles"},
    {"category_id": 10, "name": "Music"},
    {"category_id": 15, "name": "Pets & Animals"},
    {"category_id": 17, "name": "Sports"},
    {"category_id": 18, "name": "Short Movies"},
    {"category_id": 19, "name": "Travel & Events"},
    {"category_id": 20, "name": "Gaming"},
    {"category_id": 21, "name": "Videoblogging"},
    {"category_id": 22, "name": "People & Blogs"},
    {"category_id": 23, "name": "Comedy"},
    {"category_id": 24, "name": "Entertainment"},
    {"category_id": 25, "name": "News & Politics"},
    {"category_id": 26, "name": "Howto & Style"},
    {"category_id": 27, "name": "Education"},
    {"category_id": 28, "name": "Science & Technology"},
    {"category_id": 29, "name": "Nonprofits & Activism"},
    {"category_id": 30, "name": "Movies"},
    {"category_id": 31, "name": "Anime / Animation"},
    {"category_id": 32, "name": "Action / Adventure"},
    {"category_id": 33, "name": "Classics"},
    {"category_id": 34, "name": "Comedy"},
    {"category_id": 35, "name": "Documentary"},
    {"category_id": 36, "name": "Drama"},
    {"category_id": 37, "name": "Family"},
    {"category_id": 38, "name": "Foreign"},
    {"category_id": 39, "name": "Horror"},
    {"category_id": 40, "name": "Sci-Fi / Fantasy"},
    {"category_id": 41, "name": "Thriller"},
    {"category_id": 42, "name": "Shorts"},
    {"category_id": 43, "name": "Shows"},
    {"category_id": 44, "name": "Trailers"},
]


class Command(BaseCommand):
    help = "Add YouTube categories to the database"

    def handle(self, *args, **kwargs):
        for category in YOUTUBE_CATEGORIES:
            obj, created = Category.objects.get_or_create(
                category_id=category["category_id"], defaults={"name": category["name"]}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Added category {category["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category {category["name"]} already exists')
                )
        self.stdout.write(self.style.SUCCESS("YouTube categories added successfully."))
