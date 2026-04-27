from django.core.management.base import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        products_data = [
            {'name': 'Laptop', 'price': 1200.00, 'discount': 10},
            {'name': 'Smartphone', 'price': 800.00, 'discount': 25},
            {'name': 'Headphones', 'price': 150.00, 'discount': 50},
            {'name': 'TV', 'price': 1500.00, 'discount': 0},
        ]
        for item in products_data:
            product, created = Product.objects.get_or_create(
                name=item['name'],
                defaults={
                    'price': item['price'],
                    'discount': item['discount'],
                    'description': 'Auto-generated'
                }
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(self.style.SUCCESS(f'{status}: {product.name}'))
