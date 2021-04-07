import json

from django.conf import settings

# from apps.cart.utils import Cart
from apps.cart.utils import get_sum_products
from apps.main.models import Product


# def cart(request):
#     return {
#         'cart': Cart(request),
#     }


def get_products_from_cookie(request):
    cookie_list = list()
    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        products_list = request.COOKIES[settings.BASKET_COOKIE_NAME]
        cookie_list = json.loads(products_list)

    product_id_list = [i['product_id'] for i in cookie_list]
    product_count_list = [i['count'] for i in cookie_list]

    products = Product.objects.filter(id__in=product_id_list)
    products_sum = get_sum_products(products, product_count_list)

    return {
        'product_list': products,
        'sum_products': products_sum,
    }
