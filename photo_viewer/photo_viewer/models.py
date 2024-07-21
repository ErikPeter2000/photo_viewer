from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Album(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

class PhotographerImage(models.Model):
    image = models.ImageField(upload_to='images/')
    preview = models.ImageField(upload_to='images/previews/', blank=True)
    date_created = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"