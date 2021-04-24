import datetime
import json

from django.template import loader
from django.utils.encoding import uri_to_iri

from apps.main.models import Product
from core import settings


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


def get_header_item_templates(basket_product_list, count_container):
    template = loader.get_template('component/product-cart.html')
    context = dict(
        product_list=basket_product_list,
        count_container=count_container,
    )
    return template.render(context)


def get_sum_products(
        products, count_products, count_without_container, product_id_list,
        count_products_small):
    products_dict = dict((product.id, product.price) for product in products)
    products_dict_small = dict(
        (product.id, product.price_two) for product in products)

    product_id_list.reverse()

    ordered_products = [
        products_dict.get(product_item_id)
        for product_item_id in product_id_list
    ]

    ordered_products_small = [
        products_dict_small.get(product_item_id)
        for product_item_id in product_id_list
    ]

    for i in ordered_products_small:
        if i is None:
            indexPriceSmall = ordered_products_small.index(i)
            ordered_products_small[indexPriceSmall] = 0

    ordered_products.reverse()
    ordered_products_small.reverse()

    sum_count = [i * j for i, j in
                 zip(map(int, ordered_products), count_products)]

    sum_count_small = [i * j for i, j in
                       zip(map(int, ordered_products_small),
                           count_products_small)]

    products_sum = sum(sum_count) + sum(sum_count_small) + (
            sum(count_without_container) * 8)
    return products_sum


def get_cookie_list_from_cookie(request):
    cookie_list = list()

    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        products_list = request.COOKIES[settings.BASKET_COOKIE_NAME]
        cookie_list = json.loads(products_list)

    return cookie_list


def get_product_list(product_id_list, cookie_list, count=1):
    product_count_list = [i['count'] for i in cookie_list]
    cookie_count_for_container = [i['count'] for i in cookie_list]
    product_count_two_list = [i['count_two'] for i in cookie_list]
    cookie_count_two_for_container = [i['count_two'] for i in cookie_list]
    products_without_container = Product.objects.filter(
        id__in=product_id_list, category__is_container=True
    ).values_list('id', flat=True)

    for i in map(int, products_without_container):
        if i in product_id_list:
            index_item = product_id_list.index(i)
            cookie_count_for_container[index_item] = 0
            cookie_count_two_for_container[index_item] = 0
    cookie_count_for_container.reverse()
    cookie_count_two_for_container.reverse()

    cookie_count_for_container_all = [
        (count + count_two)
        for count, count_two in zip(
            cookie_count_for_container, cookie_count_two_for_container)
    ]

    products = Product.objects.filter(id__in=product_id_list)
    products_dict = dict((product.id, product) for product in products)
    product_count_list.reverse()
    product_id_list.reverse()
    product_count_two_list.reverse()

    ordered_products = [
        products_dict.get(product_item_id)
        for product_item_id in product_id_list
    ]

    basket_prod_list = [
        (count_two, count, prod)
        for count_two, count, prod in zip(
            product_count_two_list, product_count_list, ordered_products)
    ]

    count_container_list = list()
    count_container_list.reverse()
    for count, count_two in zip(
            cookie_count_for_container, product_count_two_list):
        count_container_list.append(count + count_two)
    count_container = sum(count_container_list)

    context = {
        "products": products,
        "basket_prod_list": basket_prod_list,
        "count_container": count_container,
        "product_count_list": product_count_list,
        "count_without_container": cookie_count_for_container_all,
        "count_products_small": product_count_two_list,
    }

    return context


def get_all_telegram_text(order, products, price, count, count_two):
    text = f"""
    Новый заказ!\n
    Имя клиента: {order.name}
    Тел клиента: {order.phone}
    Итого: {price}\n\n"""

    for product in products:
        index_prod = products.index(product)
        dish_name = f'{product.title}\n' \
                    f'{product.portion} - {product.price} сом - {count[index_prod]} порций\n'
        if product.price_two:
            dish_name += f'{product.portion_two} - {product.price_two} сом - {count_two[index_prod]} порций\n'
        text += dish_name + '\n'

    return text
