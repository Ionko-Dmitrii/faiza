from django.contrib import admin
from django.template import loader
from django.urls import reverse_lazy

from apps.cart.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_product_display', 'product', 'order', 'price_big',
                       'quantity_big', 'price_small', 'quantity_small',)
    fields = ('get_product_display', 'order',
              ('price_big', 'quantity_big'), ('price_small', 'quantity_small'))

    def has_add_permission(self, request, *args, **kwargs):
        return False

    def has_delete_permission(self, request, *args, **kwargs):
        return False

    def get_product_display(self, obj):
        template = loader.get_template(
            'component/product_display_in_admin.html')
        context = dict(
            image=obj.product.image.url,
            title=obj.product.title,
        )
        return template.render(context=context)

    get_product_display.short_description = 'Изображение'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'phone', 'comment', 'price', 'count_container')
    inlines = [OrderItemInline]

    # def has_delete_permission(self, request, *args, **kwargs):
    #     return False
