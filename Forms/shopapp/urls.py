from django.urls import path

from .views import shop_index, products_list, orders_list, product_create, order_create

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='index'),
    path("products/", products_list, name="products_list"),
    path("products/create", product_create, name="product_create"),
    path("orders/", orders_list, name="orders_list"),
    path("orders/create", order_create, name="order_create"),
]
