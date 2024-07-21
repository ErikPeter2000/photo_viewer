from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View, generic
from .models import Album

MAX_ALBUMS = 5
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Album

MAX_ALBUMS = 5  # Assuming MAX_ALBUMS is defined somewhere

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'photo_viewer/index.html'
    context_object_name = 'latest_album_list'
    login_url = 'accounts/login/'  # Optional: specify the login URL

    def get_queryset(self):
        return Album.objects.order_by('-date_created')[:MAX_ALBUMS]

@login_required
def profile_view(request):
    return render(request, 'photo_viewer/profile.html')