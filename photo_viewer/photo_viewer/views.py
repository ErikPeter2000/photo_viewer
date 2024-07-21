from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages
from django.views import View, generic
from .models import Album, PhotographerImage
from .storage import create_image_preview

MAX_ALBUMS = 5

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Album

MAX_ALBUMS = 5


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "photo_viewer/index.html"
    context_object_name = "latest_album_list"
    login_url = "accounts/login/"

    def get_queryset(self):
        return Album.objects.order_by("-date_created")[:MAX_ALBUMS]


class AlbumDetailView(LoginRequiredMixin, View):
    template_name = "photo_viewer/album_detail.html"
    login_url = "accounts/login/"
    context_object_name = "images_list"

    def get(self, request, *args, **kwargs):
        album = Album.objects.get(id=kwargs["album_id"])
        user_id = request.user.id
        images = PhotographerImage.objects.filter(album_id=album.id)
        return render(
            request,
            self.template_name,
            {"album": album, "images_list": images, "user_id": user_id},
        )


class ImageDetailView(LoginRequiredMixin, View):
    template_name = "photo_viewer/image_detail.html"
    login_url = "accounts/login/"

    def get(self, request, *args, **kwargs):
        image = PhotographerImage.objects.get(id=kwargs["image_id"])
        photographer_name = (
            f"{image.owner.first_name} {image.owner.last_name} ({image.owner.username})"
        )
        return render(
            request,
            self.template_name,
            {
                "image": image,
                "uploaded_by": str(photographer_name),
                "uploaded_at": str(image.date_created),
            },
        )


@require_POST
@login_required
def upload_images(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    images = request.FILES.getlist("images")
    if len(images) == 0:
        return JsonResponse({"message": "Please upload an image."}, status=200)
    for image in images:
        preview = create_image_preview(image)
        PhotographerImage.objects.create(
            image=image,
            album=album,
            date_created=datetime.now(),
            owner=request.user,
            preview=preview,
        )
    messages.success(
        request,
        f"{len(images)} Image{'s' if len(images) > 1 else ''} uploaded successfully.",
    )
    return JsonResponse({"message": "Images uploaded successfully"}, status=200)


@require_POST
@login_required
def delete_image(request, *args, **kwargs):
    image_id = kwargs["image_id"]
    try:
        image = get_object_or_404(PhotographerImage, pk=image_id)
        if (not request.user == image.owner) and (not request.user.is_superuser):
            messages.error(request, "You are not authorized to delete this image.")
            return JsonResponse(
                {"message": "You are not authorized to delete this image"}, status=403
            )
        image.delete()
        messages.success(request, "Image deleted successfully.")
        return JsonResponse({"message": "Image deleted successfully"}, status=200)
    except:
        messages.error(request, "Image not found.")
        return JsonResponse({"message": "Image not found"}, status=404)


@login_required
def profile_view(request):
    return render(request, "photo_viewer/profile.html")
