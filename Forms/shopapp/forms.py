from django import forms
from django.core import validators

from .models import Product, Order

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100, required=True)
#     price = forms.DecimalField(min_value=1, max_value=100_000,
#                                decimal_places=2, required=True)
#     description = forms.CharField(
#         label='Product description',
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 50}),
#         validators=[
#             validators.RegexValidator(
#                 regex=r'\!$',
#                 message='Description must ends with "!"'
#             )
#         ]
#     )
#     discount = forms.IntegerField()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'promocode', 'user', 'products']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = Product.objects.filter(archived=False)
