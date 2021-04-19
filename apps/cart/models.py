from django.core.validators import RegexValidator
from django.db import models

from apps.main.models import Product


class Order(models.Model):
    class Meta:
        verbose_name = 'Оформление заказа'
        verbose_name_plural = 'Оформление заказа'

    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(
        max_length=15, validators=[RegexValidator(
            regex=r'^\+996\d{9}$', message='Формат номера! +996555123123', )],
        verbose_name='Телефон',
    )
    comment = models.TextField(blank=True, null=True,
                               verbose_name='Комментарий')
    price = models.PositiveIntegerField(default=0,
                                        verbose_name='Итого к оплате')
    count_container = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Колличество контейнеров'
    )

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    product = models.ForeignKey(
        to=Product, on_delete=models.SET_NULL, verbose_name='Товар', null=True,
        related_name='product_order_item'
    )
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, verbose_name='Заказ', null=True,
        related_name='order_order_item'
    )
    quantity_big = models.PositiveIntegerField(
        default=0, verbose_name='Колличество большой порции'
    )
    quantity_small = models.PositiveIntegerField(
        default=0, verbose_name='Колличество маленькой порции'
    )
    price_big = models.PositiveIntegerField(
        default=0, verbose_name='Стоимость большой порции'
    )
    price_small = models.PositiveIntegerField(
        default=0, verbose_name='Стоимость маленькой порции'
    )

    def __str__(self):
        return self.product.title
