from django.db import models


class Category(models.Model):
    category_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
