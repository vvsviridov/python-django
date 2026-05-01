import json

from io import TextIOWrapper
from csv import DictReader

from django.contrib.auth.models import User

from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding
    )
    reader = DictReader(csv_file)
    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    orders = []
    csv_file = TextIOWrapper(
        file,
        encoding=encoding
    )
    reader = DictReader(csv_file)
    for row in reader:
        user_obj = User.objects.get(username=row['user'])
        order = Order.objects.create(
            user=user_obj,
            delivery_address=row['delivery_address'],
            promocode=row.get('promocode', ''),
        )
        product_pks = json.loads(row['products'])
        products_qs = Product.objects.filter(pk__in=product_pks)
        order.products.set(products_qs)
        orders.append(order)
    return orders
