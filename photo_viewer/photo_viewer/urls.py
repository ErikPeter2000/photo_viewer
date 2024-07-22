"""
URL configuration for photo_viewer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('albums/<int:album_id>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('albums/<int:album_id>/upload_image/', views.upload_images, name='upload_image'),
    path('albums/<int:album_id>/images/<int:image_id>', views.ImageDetailView.as_view(), name='image_detail'),
    path('albums/<int:album_id>/images/<int:image_id>/delete', views.delete_image, name='delete_image'),
    path('albums/<int:album_id>/images/<int:image_id>/report', views.ReportImageView.as_view(), name='report_image'),
    path('accounts/delete_media/', views.delete_all_user_images, name='delete_media'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
