from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from solo.models import SingletonModel

from apps.main.mixins import SliderAbstractModel
from apps.main.utils import get_product_upload_path


class MainBanner(models.Model):
    image = models.ImageField(verbose_name='Главный баннер', blank=True,
                              null=True, upload_to='main-banner')

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннер'


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=255)
    is_container = models.BooleanField(
        default=False, verbose_name='Не должно быть контейнера?'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Категория блюда'
        verbose_name_plural = 'Категории блюд'

    def get_absolute_url(self):
        return reverse('menu-category', kwargs={'pk': self.id})

    def ajax_absolute_url(self):
        return reverse('category_url', kwargs={'pk': self.id})


class Product(models.Model):
    title = models.CharField(verbose_name='Название блюда', max_length=255,
                             null=True)
    description = models.TextField(verbose_name='Описание блюда')
    category = models.ForeignKey(to=Category, verbose_name='Категория',
                                 on_delete=models.CASCADE, null=True,
                                 blank=True,
                                 related_name='category_product')
    is_available = models.BooleanField(verbose_name='Есть в наличии?',
                                       default=True)
    portion = models.CharField(verbose_name='Порция', max_length=50, null=True)
    image = models.ImageField(verbose_name="Изображение", null=True,
                              upload_to=get_product_upload_path)
    price = models.DecimalField(verbose_name='Цена', max_digits=14,
                                decimal_places=0, null=True, )
    portion_two = models.CharField(verbose_name='Пол порции', max_length=50,
                                   null=True, blank=True)
    price_two = models.DecimalField(verbose_name='Цена', max_digits=14,
                                    decimal_places=0, null=True, blank=True)
    is_populate = models.BooleanField(verbose_name='Популярное?', default=False)

    def get_absolute_url(self):
        return reverse('product_url', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class AboutUs(SingletonModel):
    class Meta:
        verbose_name = 'Старница о нас'
        verbose_name_plural = 'Старница о нас'

    banner = models.ImageField(
        verbose_name='Баннер', null=True, upload_to=get_product_upload_path
    )
    description_main = models.TextField(
        verbose_name='Текст на главной', null=True
    )
    description_one = RichTextField(verbose_name='Текст№1', null=True)
    description_two = RichTextField(verbose_name='Текст№2', null=True)
    description_three = RichTextField(verbose_name='Текст№3', null=True)
    description_four = RichTextField(verbose_name='Текст№4', null=True)

    def __str__(self):
        return str(self.banner.name)


class SliderAboutUsOne(models.Model):
    class Meta:
        verbose_name = 'Слайдер для страницы о нас №1'
        verbose_name_plural = 'Слайдер для страницы о нас №1'

    text = models.TextField(verbose_name='Текст', null=True)

    def __str__(self):
        return str(self.text)


class SliderAboutUsTwo(SliderAbstractModel):
    class Meta:
        verbose_name = 'Слайдер для страницы о нас №2'
        verbose_name_plural = 'Слайдер для страницы о нас №2'

    def __str__(self):
        return str(self.image.name)


class SliderAboutUsThree(SliderAbstractModel):
    class Meta:
        verbose_name = 'Слайдер для страницы о нас №3'
        verbose_name_plural = 'Слайдер для страницы о нас №3'

    def __str__(self):
        return str(self.image.name)


class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    name = models.CharField(
        verbose_name="Название кафе", max_length=255, null=True,
    )
    phone = models.CharField(
        verbose_name="Телефон кафе", max_length=25, null=True
    )
    address = models.CharField(
        verbose_name="Адрес кафе", max_length=255, null=True,
    )

    def __str__(self):
        return str(self.name)


class Schedule(models.Model):
    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'График работы'

    text = models.CharField(
        verbose_name="График работы", max_length=255, null=True,
    )

    def __str__(self):
        return str(self.text)


class Delivery(models.Model):
    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    text = models.CharField(
        verbose_name="Доставка", max_length=255, null=True,
    )

    def __str__(self):
        return str(self.text)
