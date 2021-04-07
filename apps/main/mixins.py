from django.db import models

from apps.main.utils import get_product_upload_path


class SliderAbstractModel(models.Model):
    """Миксин даты для моделей"""

    class Meta:
        abstract = True

    image = models.ImageField(
        verbose_name='Слайдер', null=True, upload_to=get_product_upload_path
    )
