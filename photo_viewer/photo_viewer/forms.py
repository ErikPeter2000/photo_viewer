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
        super(PhotographerImageForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        if not self.request.user or not self.request.user.is_authenticated:
            messages.error(self.request, 'You must be logged in to upload an image.')
        instance = super().save(commit=False)
        instance.date_created = datetime.now()
        instance.owner_id = self.request.user.id
        if commit:
            instance.save()
            messages.success(self.request, 'Image uploaded successfully.')
        else:
            messages.success(self.request, 'Image created successfully, and was not committed.')
        return instance