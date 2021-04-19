import json

from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.template import loader
from django.utils.encoding import uri_to_iri
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from apps.cart.forms import OrderForm
from apps.cart.models import OrderItem, Order
from apps.cart.utils import get_header_item_templates, set_cookie, \
    get_sum_products, get_cookie_list_from_cookie, get_product_list
from apps.main.models import MainBanner, Product, Category, AboutUs, \
    SliderAboutUsOne, SliderAboutUsTwo, SliderAboutUsThree, Contact


class MainPageView(TemplateView):
    template_name = 'page/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_banner'] = MainBanner.objects.first()
        context['about_us_text'] = AboutUs.objects.first()
        context['categories'] = (
            Category.objects.all()
                .prefetch_related(
                Prefetch('category_product',
                         Product.objects.filter(
                             is_populate=True,
                             is_available=True))
            )
        )

        return context


class ProductListView(ListView):
    template_name = 'page/category_detail.html'
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_category'] = Category.objects.get(id=self.kwargs['pk'])
        return context


class MenuPageView(View):
    render_template_name = 'component/render_products.html'

    def get(self, request, *args, **kwargs):
        """Подгрузка продуктов для категирии ajax"""
        category_id = request.GET.get('categoryId')
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category_id)
        products_html = loader.render_to_string(
            self.render_template_name, {
                'products': products,
                'category': category,
            })
        return JsonResponse({'render_products_html': products_html})


class ProductPreviewView(View):
    render_template_name = 'component/modal__dish-card-detail.html'

    def get(self, request, *args, **kwargs):
        """Подгрузка превью товара ajax"""
        product_id = request.GET.get('productId')
        product = Product.objects.filter(id=product_id).first()
        product_html = loader.render_to_string(
            self.render_template_name,
            {'product': product}
        )

        return JsonResponse({
            'rendered_html': product_html,
        })


class AboutUsView(TemplateView):
    template_name = 'page/about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_us'] = AboutUs.objects.first()
        context['slider_one'] = SliderAboutUsOne.objects.all()
        context['slider_two'] = SliderAboutUsTwo.objects.all()
        context['slider_three'] = SliderAboutUsThree.objects.all()
        context['categories'] = Category.objects.all()

        return context


class ContactView(TemplateView):
    template_name = 'partials/footer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.all()

        return context


class BasketActionView(View):

    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)
        count = 1
        count_two = 0

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]
        cookie_count = [i['count'] for i in cookie_list]
        product_count_two_list = [i['count_two'] for i in cookie_list]

        if product_id in product_id_list:
            index_item = product_id_list.index(product_id)
            count_two = product_count_two_list[index_item]
            if product_count_two_list[index_item] < 1:
                del cookie_list[index_item]
                product_id_list.remove(product_id)
            else:
                if cookie_count[index_item] > 0:
                    product_dict = dict(
                        product_id=product_id,
                        count=0,
                        count_two=count_two,
                    )
                    cookie_list[index_item] = product_dict
                else:
                    product_dict = dict(
                        product_id=product_id,
                        count=count,
                        count_two=count_two,
                    )
                    cookie_list[index_item] = product_dict
        else:
            product_id_list.append(product_id)
            product_dict = dict(
                product_id=product_id,
                count=count,
                count_two=count_two,
            )
            cookie_list.append(product_dict)

        context_products = get_product_list(product_id_list, cookie_list)

        context = dict(
            header_item=get_header_item_templates(
                context_products["basket_prod_list"],
                context_products["count_container"]
            ),
            sum_products=get_sum_products(
                context_products["products"],
                context_products["product_count_list"],
                context_products["count_without_container"],
                product_id_list,
                context_products["count_products_small"],
            ),
        )

        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class BasketActionTwoView(View):

    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)
        count = 0
        count_two = 1

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]
        product_count_list = [i['count'] for i in cookie_list]
        product_count_two_list = [i['count_two'] for i in cookie_list]

        if product_id in product_id_list:
            index_item = product_id_list.index(product_id)
            count = product_count_list[index_item]
            if product_count_list[index_item] < 1:
                del cookie_list[index_item]
                product_id_list.remove(product_id)
            else:
                if product_count_two_list[index_item] > 0:
                    product_dict = dict(
                        product_id=product_id,
                        count=count,
                        count_two=0,
                    )
                    cookie_list[index_item] = product_dict
                else:
                    product_dict = dict(
                        product_id=product_id,
                        count=count,
                        count_two=count_two,
                    )
                    cookie_list[index_item] = product_dict
        else:
            product_id_list.append(product_id)
            product_dict = dict(
                product_id=product_id,
                count=count,
                count_two=count_two,
            )
            cookie_list.append(product_dict)

        context_products = get_product_list(product_id_list, cookie_list, count)

        context = dict(
            header_item=get_header_item_templates(
                context_products['basket_prod_list'],
                context_products['count_container'],
            ),
            sum_products=get_sum_products(
                context_products['products'],
                context_products["product_count_list"],
                context_products["count_without_container"],
                product_id_list,
                context_products['count_products_small'],
            ),
        )

        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class ClearBasketView(View):

    def post(self, request, *args, **kwargs):
        cookie_list = []
        count_container = []
        context = dict(
            clear_basket=get_header_item_templates(cookie_list,
                                                   count_container),
            sum_products=0,
        )
        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))
        return response


class UpdateQuantityView(View):

    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)
        product_id_list = [i['product_id'] for i in cookie_list]
        product_id = int(request.POST.get('productId'))
        index_product = product_id_list.index(product_id)

        if request.POST.get('count'):
            count = int(request.POST.get('count'))
        else:
            count_list = [i['count'] for i in cookie_list]
            count = count_list[index_product]

        if request.POST.get('count_two'):
            count_two = int(request.POST.get('count_two'))
        else:
            count_two_list = [i['count_two'] for i in cookie_list]
            count_two = count_two_list[index_product]

        product_dict = dict(
            product_id=product_id,
            count=count,
            count_two=count_two
        )

        product_count_list = [i['count'] for i in cookie_list]
        if request.POST.get('count'):
            product_count_list[index_product] = int(request.POST.get('count'))
        else:
            product_count_list[index_product] = int(
                request.POST.get('count_two'))
        cookie_list[index_product] = product_dict
        context_products = get_product_list(product_id_list, cookie_list, count)
        product_count_list.reverse()
        count_container = sum(context_products["count_without_container"])

        context = dict(
            count_product=count_container,
            sum_products=get_sum_products(
                context_products["products"],
                context_products["product_count_list"],
                context_products["count_without_container"],
                product_id_list,
                context_products["count_products_small"],
            ),
        )

        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class BasketRemoveProduct(View):
    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]

        if product_id in product_id_list:
            index_item = product_id_list.index(product_id)
            del cookie_list[index_item]
            product_id_list.remove(product_id)

        context_products = get_product_list(product_id_list, cookie_list)

        context = dict(
            header_item=get_header_item_templates(
                context_products["basket_prod_list"],
                context_products["count_container"]
            ),
            sum_products=get_sum_products(
                context_products["products"],
                context_products["product_count_list"],
                context_products["count_without_container"],
                product_id_list,
                context_products["count_products_small"],
            ),
        )

        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class BasketAddRemoveProductBig(View):
    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)
        count_two = [i['count_two'] for i in cookie_list]
        count = [i['count'] for i in cookie_list]

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]
        index_item = product_id_list.index(product_id)

        if count[index_item] > 0:
            if count_two[index_item] > 0:
                count = 0,
                product_dict = dict(
                    product_id=product_id,
                    count=0,
                    count_two=count_two[index_item],
                )
                cookie_list[index_item] = product_dict
            else:
                count = 1,
                product_dict = dict(
                    product_id=product_id,
                    count=1,
                    count_two=count_two[index_item],
                )
                cookie_list[index_item] = product_dict

        else:
            count = 1,
            product_dict = dict(
                product_id=product_id,
                count=1,
                count_two=count_two[index_item],
            )
            cookie_list[index_item] = product_dict

        context_products = get_product_list(product_id_list, cookie_list)
        count_container = sum(context_products["count_without_container"])

        context = dict(
            count_product=count_container,
            sum_products=get_sum_products(
                context_products["products"],
                context_products["product_count_list"],
                context_products["count_without_container"],
                product_id_list,
                context_products["count_products_small"],
            ),
            count_one=count,
        )

        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class BasketAddRemoveProductSmall(View):
    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)
        count_two = [i['count_two'] for i in cookie_list]
        count = [i['count'] for i in cookie_list]

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]
        index_item = product_id_list.index(product_id)

        if count_two[index_item] > 0:
            if count[index_item] > 0:
                count_two = 0,
                product_dict = dict(
                    product_id=product_id,
                    count=count[index_item],
                    count_two=0,
                )
                cookie_list[index_item] = product_dict
            else:
                count_two = 1,
                product_dict = dict(
                    product_id=product_id,
                    count=count[index_item],
                    count_two=1,
                )
                cookie_list[index_item] = product_dict
        else:
            count_two = 1,
            product_dict = dict(
                product_id=product_id,
                count=count[index_item],
                count_two=1,
            )
            cookie_list[index_item] = product_dict

        context_products = get_product_list(product_id_list, cookie_list)
        count_container = sum(context_products["count_without_container"])

        context = dict(
            count_product=count_container,
            sum_products=get_sum_products(
                context_products["products"],
                context_products["product_count_list"],
                context_products["count_without_container"],
                product_id_list,
                context_products["count_products_small"],
            ),
            count_two=count_two,
        )

        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class OrderView(CreateView):
    template_name = 'component/modal__ordering.html'
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        cookie_list = get_cookie_list_from_cookie(request)
        order = self.form_class(json.loads(request.POST.get('form_fields')))
        price = request.POST.get('product_sum')
        count_container = request.POST.get('count_container')
        product_ids = [i['product_id'] for i in cookie_list]
        count = [i['count'] for i in cookie_list]
        count_two = [i['count_two'] for i in cookie_list]
        products = Product.objects.filter(id__in=product_ids)
        order_items = []
        product_dict = dict((product.id, product) for product in products)
        ordered_products = [
            product_dict.get(product_item_id)
            for product_item_id in product_ids
        ]
        sum_container = int(count_container)*8

        if order.is_valid():
            order_model = order.save(commit=False)
            order_model.price = price
            order_model.count_container = f'{count_container}шт.*8сом = {sum_container}сом'
            order_model.save()

            for product in ordered_products:
                if product.price_two:
                    price_two = product.price_two
                else:
                    price_two = 0
                index_prod = ordered_products.index(product)
                order_items.append(
                    OrderItem(
                        product=product, order=order_model,
                        quantity_big=count[index_prod],
                        quantity_small=count_two[index_prod],
                        price_big=product.price,
                        price_small=price_two,
                    )
                )

            OrderItem.objects.bulk_create(order_items)

            clear_basket = ClearBasketView()

            response = clear_basket.post(self.request, *args, **kwargs)

            return response
        else:
            order = self.form_class(json.loads(request.POST.get('form_fields')))
            message = []

            for item in order.errors:
                message.append([item, order.errors[item]])

            return JsonResponse(
                dict(success=False, message=message), status=400
            )
