from datetime import datetime
from django import forms
from .models import PhotographerImage, Album
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class PhotographerImageForm(forms.ModelForm):
    class Meta:
        model = PhotographerImage
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.album_id = kwargs.pop('album_id', None)
        super(PhotographerImageForm, self).__init__(*args, **kwargs)