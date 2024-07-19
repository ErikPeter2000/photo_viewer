from django.db import models
from datetime import datetime

class Photographer(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField
    def __init__(self, name: str):
        self.name = name
        self.date_added = datetime.now()

class ImageReference(models.Model):
    image_name = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    ownerId = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    def __init__(self, image_name: str, ownerId: int = None):
        self.image_name = models.CharField(max_length=255, primary_key=True)
        self.date_added = datetime.now()
        self.ownerId = ownerId
        
class Album(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField
    ownerId = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    def __init__(self, name: str, ownerId: int):
        self.name = name
        self.date_added = datetime.now()
        self.ownerId = ownerId