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
        # self.fields['products'].queryset = Product.objects.only('id', 'name')
        self.fields['products'].queryset = Product.objects.filter(archived=False)


# class AuditMixin:
#     """
#     Миксин для автоматического заполнения полей created_by и updated_by.
#     Используется в ModelForm.
#     Требует, чтобы форма получила request через инициализацию.
#     """

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)  # ← извлекаем request из kwargs
#         super().__init__(*args, **kwargs)

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if self.request and self.request.user.is_authenticated:
#             if not instance.pk:  # если объект новый
#                 instance.created_by = self.request.user
#             instance.updated_by = self.request.user
#         if commit:
#             instance.save()
#             self.save_m2m()  # важно для ManyToManyField
#         return instance

# class OrderForm(AuditMixin, forms.ModelForm):
    # ... поля формы


# class SecureForm(forms.Form):
#     # Защита от массового присвоения
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
   
#     # CSRF защита для AJAX-форм
#     @method_decorator(requires_csrf_token)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)