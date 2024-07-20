from django.db import models
from datetime import datetime

class Photographer(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

class ImageReference(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    ownerId = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"
        
class Album(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    ownerId = models.ForeignKey(Photographer, on_delete=models.CASCADE)    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"