from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),  # Цена не может быть отрицательной
        ],
    )
    discount = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),  # Скидка не может быть больше 100%
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='products'
    )
    archived = models.BooleanField(default=False)

    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self):
        return f'{self.name} ${self.price} {self.discount}%'


class Order(models.Model):
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f'Order #{self.pk} by {self.user}'
