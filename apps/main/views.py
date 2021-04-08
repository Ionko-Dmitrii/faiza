import json

from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.template import loader
from django.views import View
from django.views.generic import TemplateView, ListView

from apps.cart.utils import get_header_item_templates, set_cookie, \
    get_sum_products
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
        cookie_list = list()
        count = 1
        if settings.BASKET_COOKIE_NAME in request.COOKIES:
            products_list = request.COOKIES[settings.BASKET_COOKIE_NAME]
            cookie_list = json.loads(products_list)

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]
        product_dict = dict(
            product_id=product_id,
            count=count
        )

        if product_id in product_id_list:
            index_item = product_id_list.index(product_id)
            del cookie_list[index_item]
            product_id_list.remove(product_id)
        else:
            product_id_list.append(product_id)
            cookie_list.append(product_dict)

        product_count_list = [i['count'] for i in cookie_list]
        products = Product.objects.filter(id__in=product_id_list)

        products_dict = dict((product.id, product) for product in products)
        product_id_list.reverse()

        ordered_products = [
            products_dict.get(product_item_id)
            for product_item_id in product_id_list
        ]

        context = dict(
            header_item=get_header_item_templates(ordered_products),
            sum_products=get_sum_products(products, product_count_list),
        )
        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class ClearBasketView(View):

    def post(self, request, *args, **kwargs):
        cookie_list = []

        products = Product.objects.filter(id__in=cookie_list)
        context = dict(
            clear_basket=get_header_item_templates(products),
        )
        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response


class UpdateQuantityView(View):

    def post(self, request, *args, **kwargs):
        cookie_list = list()
        count = int(request.POST.get('count'))

        if settings.BASKET_COOKIE_NAME in request.COOKIES:
            products_list = request.COOKIES[settings.BASKET_COOKIE_NAME]
            cookie_list = json.loads(products_list)

        product_id = int(request.POST.get('productId'))
        product_id_list = [i['product_id'] for i in cookie_list]
        product_dict = dict(
            product_id=product_id,
            count=count
        )

        product_count_list = [i['count'] for i in cookie_list]
        index_item2 = product_id_list.index(product_id)
        product_count_list[index_item2] = int(request.POST.get('count'))

        cookie_list[index_item2] = product_dict

        products = Product.objects.filter(id__in=product_id_list)
        context = dict(
            sum_products=get_sum_products(products, product_count_list),
        )
        response = JsonResponse(context)
        set_cookie(response, settings.BASKET_COOKIE_NAME,
                   json.dumps(cookie_list))

        return response
