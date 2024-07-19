from django.views import View, generic
from .models import Album

MAX_ALBUMS = 5
    
class IndexView(generic.ListView):
    template_name = 'photo_viewer/index.html'
    context_object_name = 'latest_album_list'

    def get_queryset(self):
        return Album.objects.order_by('-date_created')[:MAX_ALBUMS]