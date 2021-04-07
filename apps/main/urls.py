from django.urls import path

from apps.main.views import (
    MainPageView, MenuPageView, ProductPreviewView, ProductListView,
    AboutUsView, ContactView
)

urlpatterns = [
    path('', MainPageView.as_view(), name='main-page'),
    path('menu/<int:pk>/', ProductListView.as_view(), name='menu-category'),
    path('product/<int:pk>/', ProductPreviewView.as_view(), name='product_url'),
    path('category/<int:pk>/', MenuPageView.as_view(), name='category_url'),
    path('about-us/', AboutUsView.as_view(), name='about_us_url'),
    path('1', ContactView.as_view(), name='contact_url'),
]
