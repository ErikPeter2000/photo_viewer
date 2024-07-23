from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from asgiref.sync import sync_to_async
from django.utils.decorators import decorator_from_middleware_with_args
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import View, generic
from django.utils import timezone
from django_user_agents.utils import get_user_agent
from .models import Album, PhotographerImage,ImageReport
from . import storage, settings
import logging
import asyncio

async_login_required = decorator_from_middleware_with_args(AuthenticationMiddleware)
MAX_DISPLAY_ALBUMS = 5
logger = logging.getLogger(__name__)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Album

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "photo_viewer/index.html"
    context_object_name = "latest_album_list"
    login_url = "accounts/login/"

    def get_queryset(self):
        return Album.objects.order_by("-date_created")[:MAX_DISPLAY_ALBUMS]


class AlbumDetailView(LoginRequiredMixin, View):
    template_name = "photo_viewer/album_detail.html"
    login_url = "accounts/login/"
    context_object_name = "images_list"

    def get(self, request, *args, **kwargs):        
        user_agent = get_user_agent(request)
        is_desktop = user_agent.is_pc
        album = Album.objects.get(id=kwargs["album_id"])
        user_id = request.user.id
        images = PhotographerImage.objects.filter(album_id=album.id).exclude(imagereport__isnull=False)
        images = self._group_by_date_taken(images)
        return render(
            request,
            self.template_name,
            {"album": album, "images_list": images, "user_id": user_id, "is_desktop": is_desktop},
        )
        
    def _group_by_date_taken(self, images):
        images_by_date = {}
        for image in images:
            date_taken = image.date_taken.strftime("%d %B %Y")
            if date_taken not in images_by_date:
                images_by_date[date_taken] = []
            images_by_date[date_taken].append(image)
        images_by_date = dict(sorted(images_by_date.items(), key=lambda x: x[0], reverse=True))
        return images_by_date

class ImageDetailView(LoginRequiredMixin, View):
    template_name = "photo_viewer/image_detail.html"
    login_url = "accounts/login/"

    def get(self, request, *args, **kwargs):
        image = PhotographerImage.objects.get(id=kwargs["image_id"])
        if ImageReport.objects.filter(image=image).exists():
            return render(request, '404.html', status=404)
        photographer_name = (
            f"{image.owner.first_name} {image.owner.last_name} ({image.owner.username})"
        )
        return render(
            request,
            self.template_name,
            {
                "image": image,
                "user_id": request.user.id,
                "uploaded_by": str(photographer_name),
                "uploaded_on": image.date_uploaded.strftime("%d %B %Y %H:%M:%S"),
                "date_taken": image.date_taken.strftime("%d %B %Y %H:%M:%S"),
            },
        )

class ReportImageView(LoginRequiredMixin, View):
    template_name = "photo_viewer/report_image.html"
    login_url = "accounts/login/"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"album_id": kwargs["album_id"], "image_id": kwargs["image_id"]})

    def post(self, request, *args, **kwargs):
        image_id = kwargs["image_id"]
        reason = request.POST.get("reason")
        description = request.POST.get("description")        
        image = get_object_or_404(PhotographerImage, pk=image_id)
        report = ImageReport(
            image=image,
            reporter=request.user,
            reason=reason,
            description=description,
            date_reported=timezone.now(),
        )
        report.save()
        messages.success(request, "Image reported successfully.")
        return JsonResponse({"message": "Image reported successfully"}, status=200)

@require_POST
async def upload_images(request, *args, **kwargs):
    album_id = kwargs["album_id"]
    album = await sync_to_async(get_object_or_404)(Album, pk=album_id)
    images = request.FILES.getlist("images")
    if len(images) == 0:
        return JsonResponse({"message": "Please upload an image."}, status=200)
    results = await storage.save_images_background(images, album, request.user)
    error_count = len([result for result in results if not result])
    if error_count == 0:
        messages.success(
            request,
            f"{len(images)} Image{'s' if len(images) > 1 else ''} uploaded successfully.",
        )
        return JsonResponse({"message": "Images uploaded successfully"}, status=200)
    else:
        messages.error(
            request,
            f"{error_count}/{len(images)} Files{'s' if error_count > 1 else ''} failed to upload.",
        )
        return JsonResponse(
            {"message": f"{error_count} Files{'s' if error_count > 1 else ''} failed to upload."},
            status=400,
        )
    

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

@require_POST
@login_required
def delete_all_user_images(request):
    user = request.user
    storage.delete_all_user_media(user)
    messages.success(request, "All images deleted successfully.")
    return JsonResponse({"message": "All images deleted successfully"}, status=200)

@require_POST
@login_required
def delete_account(request):
    user = request.user
    storage.delete_all_user_media(user)
    user.delete()
    messages.success(request, "Account deleted successfully.")
    return JsonResponse({"message": "Account deleted successfully"}, status=200)

@login_required
def profile_view(request):
    return render(request, "photo_viewer/profile.html")

def about_view(request):
    return render(request, "photo_viewer/about.html", {"credits": settings.CREDITS})