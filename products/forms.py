from django import forms
from .models import Product, ProductVariant


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'base_price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter product name',
            'autofocus': 'autofocus'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Enter product description',
            'rows': 4
        })
        self.fields['base_price'].widget.attrs.update({
            'placeholder': 'Enter base price',
            'step': '0.01',
            'min': '0'
        })


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'color', 'price', 'stock', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['price'].widget.attrs.update({
            'placeholder': 'Variant price',
            'step': '0.01',
            'min': '0'
        })
        self.fields['stock'].widget.attrs.update({
            'placeholder': 'Available stock',
            'min': '0'
        })
