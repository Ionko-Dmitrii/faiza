import datetime

from django.template import loader


# class Cart:
#     product_list = list()
#
#     def __init__(self, request, *args, **kwargs):
#         self.product_list = list()


def set_cookie(response, key, value, days_expire=60):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT"
    )
    response.set_cookie(key, value, max_age=max_age, expires=expires)
    return response


def get_header_item_templates(basket_product_list):
    template = loader.get_template('component/product-cart.html')
    context = dict(product_list=basket_product_list)
    return template.render(context)


def get_sum_products(products, count_product):
    products_prices = products.values_list('price', flat=True)

    sum_count = list()
    for i, j in zip(map(int, products_prices), count_product):
        sum_count.append(i * j)

    products_sum = sum(sum_count) + (sum(count_product) * 8)

    return products_sum
