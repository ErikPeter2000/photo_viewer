from django.core.management.base import BaseCommand, CommandError, CommandParser

from ... import settings, models, storage
from ...models import PhotographerImage
import os
import shutil

class Command(BaseCommand):
    help = "Deletes files in the media directory and deletes PhotographerImage objects"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('--all', help="Delete all media files and database objects", action="store_true")
    
    def handle(self, *args, **options):
        if options.get("all"):
            storage.delete_all_media()
            print("All media files have been deleted.")
        else:
            storage.delete_unreferenced_media()
            print("All unreferenced media files have been deleted.")