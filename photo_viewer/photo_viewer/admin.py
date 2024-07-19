from django.contrib import admin
from .models import Album, ImageReference, Photographer

admin.site.register(Album)
admin.site.register(ImageReference)
admin.site.register(Photographer)