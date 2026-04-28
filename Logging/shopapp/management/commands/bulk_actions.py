from django.core.management.base import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User

from typing import Sequence

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo bulk actions')

        result = Product.objects.filter(
            name__contains='smartfone',
        ).update(discount=10)
        print(result)

        # info = [
        #     ('smartfone 1', 199),
        #     ('smartfone 2', 299),
        #     ('smartfone 3', 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)

        # for obj in result:
        #     print(obj)

        self.stdout.write('End demo')
