from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View, generic
from .models import Album

MAX_ALBUMS = 5
    
class IndexView(generic.ListView):
    template_name = 'photo_viewer/index.html'
    context_object_name = 'latest_album_list'

    def get_queryset(self):
        return Album.objects.order_by('-date_created')[:MAX_ALBUMS]

@login_required
def profile_view(request):
    return render(request, 'photo_viewer/profile.html')