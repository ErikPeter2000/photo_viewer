from PIL import Image, ExifTags, ImageFile
from django.core.files import File
from io import BytesIO
from .models import PhotographerImage
from django.utils import timezone
import logging
from concurrent.futures import ThreadPoolExecutor
from . import settings
import os
import shutil

ImageFile.LOAD_TRUNCATED_IMAGES = True
PREVIEW_SIZE = (200, 200)
MAX_WORKERS = 4
logger = logging.getLogger(__name__)


def batch_save_images_background(images, album, user):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(try_save_image, image, album, user) for image in images
        ]
        results = [future.result() for future in futures]
    return results


def try_save_image(image, album, user):
    try:
        preview = create_image_preview(image)
        date_taken = get_image_taken_date(image)
        PhotographerImage.objects.create(
            image=image,
            album=album,
            date_uploaded=timezone.now(),
            date_taken=date_taken if date_taken else timezone.now(),
            owner=user,
            preview=preview,
        )
        logger.info(f"Image uploaded: {image.name}")
        return True
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return False


def get_image_taken_date(image_file):
    with Image.open(image_file) as image:
        try:
            for exif in image._getexif().items():
                if ExifTags.TAGS.get(exif[0]) == "DateTimeOriginal":
                    date_str = exif[1]
                    return timezone.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        except AttributeError:
            return None
    return None


def create_image_preview(image_file, size=PREVIEW_SIZE):
    with Image.open(image_file) as image:
        # rotate the image if necessary
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            exif = dict(image._getexif().items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        # crop to a square
        width, height = image.size
        new_size = min(width, height)
        start_x = (width - new_size) // 2
        start_y = (height - new_size) // 2
        end_x = start_x + new_size
        end_y = start_y + new_size
        image = image.crop((start_x, start_y, end_x, end_y))
        # shrink
        image.thumbnail(size)

        # save the image to a BytesIO object
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        image_file = File(image_io, name=image_file.name)

        return image_file


def delete_all_user_media(user):
    images = PhotographerImage.objects.filter(owner=user)
    for image in images:
        image.delete()
    logger.info(f"All media files for user {user.username} have been deleted.")


def delete_unreferenced_media():
    images = PhotographerImage.objects.all()
    media_dir = os.path.join(settings.BASE_DIR, "media")
    for image in images:
        if not os.path.exists(os.path.join(media_dir, image.image.name)):
            image.delete()
            logger.info(f"Deleted unreferenced media file: {image.image.name}")
    logger.info("All unreferenced media files have been deleted.")


def delete_all_media():
    PhotographerImage.objects.all().delete()
    media_dir = os.path.join(settings.BASE_DIR, "media")
    shutil.rmtree(media_dir)
    make_media_dirs()
    logger.info("All media files have been deleted.")


def make_media_dirs():
    media_dir = os.path.join(settings.BASE_DIR, "media")
    if not os.path.exists(media_dir):
        os.mkdir(media_dir)
    images_dir = os.path.join(media_dir, "images")
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)
    preview_dir = os.path.join(images_dir, "previews")
    if not os.path.exists(preview_dir):
        os.mkdir(preview_dir)
    logger.info("Media directories have been created.")
