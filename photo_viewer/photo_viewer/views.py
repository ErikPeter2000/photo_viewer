from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import View, generic
from .models import Album, PhotographerImage
from .forms import PhotographerImageForm

MAX_ALBUMS = 5
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Album

MAX_ALBUMS = 5

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'photo_viewer/index.html'
    context_object_name = 'latest_album_list'
    login_url = 'accounts/login/'

    def get_queryset(self):
        return Album.objects.order_by('-date_created')[:MAX_ALBUMS]

class AlbumDetailView(LoginRequiredMixin, View):
    template_name = 'photo_viewer/album_detail.html'
    login_url = 'accounts/login/'
    context_object_name = 'images_list'

    def get(self, request, *args, **kwargs):
        album = Album.objects.get(id=kwargs['pk'])
        images = PhotographerImage.objects.filter(album_id=album.id)
        print("images found:", len(images))
        return render(request, self.template_name, {'album': album, 'images_list': images})

@require_POST
@login_required
def upload_images(request, pk):
    album = get_object_or_404(Album, pk=pk)
    images = request.FILES.getlist('images')
    for image in images:
        PhotographerImage.objects.create(image=image, album=album, date_created=datetime.now(), owner=request.user)
    return JsonResponse({'message': 'Images uploaded successfully'}, status=200)

@login_required
def profile_view(request):
    return render(request, 'photo_viewer/profile.html')