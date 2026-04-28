from django.core.management.base import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User

from typing import Sequence

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo')

        users_info = User.objects.values_list('username', flat=True)
        for u in users_info:
            print(u)

        # product_values = Product.objects.values('pk', 'name')
        # for p in product_values:
        #     print(p)

        self.stdout.write('End demo')
