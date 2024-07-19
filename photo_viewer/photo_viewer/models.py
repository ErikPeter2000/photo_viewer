from django.db import models
from datetime import datetime

class Photographer(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField()

class ImageReference(models.Model):
    image_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    ownerId = models.ForeignKey(Photographer, on_delete=models.CASCADE)
        
class Album(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    ownerId = models.ForeignKey(Photographer, on_delete=models.CASCADE)