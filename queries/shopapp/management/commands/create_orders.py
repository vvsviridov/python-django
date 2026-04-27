from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from django.db import transaction

from typing import Sequence

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username="admin")
        # products: Sequence[Product] = Product.objects.defer('description', 'price', 'created_at').all()
        products: Sequence[Product] = Product.objects.only('id').all()

        # order, created = Order.objects.get_or_create(
        #     user=user,
        #     delivery_address="Lenina St. 123",
        #     defaults={"promocode": "SALE"}
        # )
        order, created = Order.objects.get_or_create(
            user=user,
            delivery_address="Marksa St. 2029",
            defaults={"promocode": "YESNO!"}
        )
        for product in products:
            order.products.add(product)
        order.save()

        self.stdout.write(
            self.style.SUCCESS(f"Order for {user.username} "
                               f"{'created' if created else 'updated'} {order}")
        )
