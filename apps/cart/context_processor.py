# from apps.cart.utils import Cart
from apps.cart.utils import (
    get_sum_products, get_cookie_list_from_cookie, get_product_list
)

# def cart(request):
#     return {
#         'cart': Cart(request),
#     }


def get_products_from_cookie(request):
    cookie_list = get_cookie_list_from_cookie(request)
    product_id_list = [i['product_id'] for i in cookie_list]
    context_products = get_product_list(product_id_list, cookie_list)

    products_sum = get_sum_products(
        context_products["products"],
        context_products["product_count_list"],
        context_products["count_without_container"],
        product_id_list,
        context_products["count_products_small"],
    )

    return {
        'product_list': context_products["basket_prod_list"],
        'sum_products': products_sum,
        'count_container': context_products["count_container"],
    }
