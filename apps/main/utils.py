import os

from django.utils.text import slugify

from transliterate import translit


def get_product_upload_path(instance, filename):
    return os.path.join('products', str(instance.id), filename)


def generate_slug(populate_field, unique_with):
    return slugify(translit(f'{populate_field}-{unique_with}', 'ru',
                            reversed=True))
