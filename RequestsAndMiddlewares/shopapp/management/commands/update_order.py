from django.core.management.base import BaseCommand
from shopapp.models import Order, Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if order is None:
            self.stdout.write('Order not found!')
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(
            self.style.SUCCESS(f"Order {order} updated {order.products.all()}")
        )
