from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    
    ProductsView,
    ProductCreateView,
    ProductUpdateView,
    ProductsDetailsView,
    ProductDeleteView,
    
    OrdersView,
    OrderCreateView,
    OrderUpdateView,
    OrderDetailsView,
    OrderDeleteView,
    ProductDataExportView,

    ProductViewSet,
    OrderViewSet,

    LatestProductsFeed,

    # product_create,
    # order_create
)

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),

    path('api/', include(routers.urls)),

    path("products/", ProductsView.as_view(), name="products_list"),
    path("products/export/", ProductDataExportView.as_view(), name="products-export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductsDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    # path("products/create", product_create, name="product_create"),
    
    path('products/latest/feed/', LatestProductsFeed(), name='feed'),
    
    path("orders/", OrdersView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
]
