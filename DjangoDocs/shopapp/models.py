from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy


def product_preview_dir_path(instance: "Product", filename: str) -> str:
    return "product/{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Product(models.Model):
    """
    Товары интернет-магазина

    Заказы тут: :model:`shopapp.Order`
    """
    class Meta:
        ordering = ['name']
        verbose_name = gettext_lazy('Product')
        verbose_name_plural = gettext_lazy('Products')

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
    archived = models.BooleanField(default=False)
    preview = models.ImageField(upload_to=product_preview_dir_path, null=True, blank=True)

    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self):
        return f'{self.name} ${self.price} {self.discount}%'


def product_images_dir_path(instance: "ProductImage", filename: str) -> str:
    return "product/{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_dir_path, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class Order(models.Model):
    class Meta:
        verbose_name = gettext_lazy('Order')
        verbose_name_plural = gettext_lazy('Orders')

    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    reciept = models.FileField(null=True, upload_to='orders/reciepts/')

    def __str__(self):
        return f'Order #{self.pk} by {self.user}'
