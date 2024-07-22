from django.contrib import admin
from django.utils.html import format_html
from .models import Album, PhotographerImage, ImageReport

admin.site.register(Album)

class ImageReportAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'image', 'image_owner', 'reporter', 'reason', 'description', 'date_reported')
    list_filter = ('reason', 'date_reported')
    search_fields = ('reason', 'description')
    date_hierarchy = 'date_reported'

    def image_preview(self, obj):
        return format_html('<img src="{}" width="150" height="auto" />', obj.image.preview.url)
    def image_owner(self, obj):
        return obj.image.owner.username
    image_preview.short_description = 'Image Preview'

class PhotographerImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'image', 'owner', 'album', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('owner', 'album')
    date_hierarchy = 'date_created'

    def image_preview(self, obj):
        return format_html('<img src="{}" width="75" height="auto" />', obj.preview.url)
    image_preview.short_description = 'Image Preview'

admin.site.register(PhotographerImage, PhotographerImageAdmin)
admin.site.register(ImageReport, ImageReportAdmin)