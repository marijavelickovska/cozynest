from django import forms
from .models import Product


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
