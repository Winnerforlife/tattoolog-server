import logging
from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction

from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


def convert_to_webp_signal(image_field_name):
    def wrapper(sender, instance, **kwargs):
        image_field = getattr(instance, image_field_name)

        if image_field and 'webp' not in image_field.path:
            original_path = image_field.path
            try:
                with transaction.atomic():
                    img = Image.open(image_field.path)
                    output = BytesIO()
                    img.save(output, format='WEBP')
                    output.seek(0)

                    file_name = image_field.name.split('/')[-1]
                    new_name = f"{file_name.rsplit('.', 1)[0]}.webp"
                    image_field.save(new_name, ContentFile(output.read()), save=False)

                    instance.save()

                if default_storage.exists(original_path):
                    default_storage.delete(original_path)

                logger.info(f"Successfully converted {original_path} to {new_name}")
            except Exception as e:
                logger.error(f"Failed to convert {original_path} to WEBP: {e}")
    return wrapper
