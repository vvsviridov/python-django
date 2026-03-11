from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username="admin")

        order, created = Order.objects.get_or_create(
            user=user,
            delivery_address="Lenina St. 123",
            defaults={"promocode": "SALE"}
        )

        self.stdout.write(
            self.style.SUCCESS(f"Order for {user.username} "
                               f"{'created' if created else 'updated'} {order}")
        )
