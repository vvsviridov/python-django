from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from .models import Product, Order


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class ProductForm(forms.ModelForm):
    images = forms.ImageField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount', 'preview', 'images']

    def clean(self):
        cleaned_data = super().clean()
        if 'images' in self._errors:
            del self._errors['images']
        return cleaned_data



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'promocode', 'user', 'products']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['products'].queryset = Product.objects.only('id', 'name')
        self.fields['products'].queryset = Product.objects.filter(archived=False)


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['csv']),
            validate_file_size
        ]
    )


def validate_file_size(file):
    maxSize = 5 * 1024 * 1024  # 5MB
    if file.size > maxSize:
        raise ValidationError('File too big')