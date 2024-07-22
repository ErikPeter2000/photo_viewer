from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Album(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

class PhotographerImage(models.Model):
    image = models.ImageField(upload_to='images/')
    preview = models.ImageField(upload_to='images/previews/', blank=True)
    date_taken = models.DateTimeField()
    date_uploaded = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.__class__.__name__}: {self.id}"
    @property
    def delete_url(self):
        return reverse("image_delete", kwargs={"album_id": self.album.id, "image_id": self.id})
    
class ImageReport(models.Model):
    image = models.ForeignKey(PhotographerImage, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=64)
    description = models.TextField()
    date_reported = models.DateTimeField()
    def __str__(self):
        return f"{self.__class__.__name__}: {self.id}"