from django.urls import path

from apps.main.views import (
    BasketActionView, ClearBasketView, UpdateQuantityView, BasketActionTwoView
)

urlpatterns = [
    path('basket/<int:pk>/', BasketActionView.as_view(), name='basket_url'),
    path('basket_two/<int:pk>/', BasketActionTwoView.as_view(),
         name='basket_two_url'),
    path('remove/<int:pk>/', BasketActionView.as_view(), name='remove_url'),
    path('clear-basket/', ClearBasketView.as_view(), name='clear_url'),
    path('update_quantity/<int:pk>/', UpdateQuantityView.as_view(),
         name='update_quantity'),
]
