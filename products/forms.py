from django import forms
from .models import Product, ProductVariant, Size


class ProductForm(forms.ModelForm):
    """
    Form for creating or updating Product instances.
    """
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'base_price', 'image']

    def __init__(self, *args, **kwargs):
        """
        Customize widgets: placeholders, autofocus, rows for description,
        and min/step for price.
        """
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
    """
    Form for creating or updating ProductVariant instances.
    Dynamically filters size choices based on product category.
    """
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'color', 'price', 'stock', 'image']

    def __init__(self, *args, **kwargs):
        variant = kwargs.get('instance', None)
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

        if variant and variant.product and variant.product.category:
            category = variant.product.category
            sizes = Size.objects.filter(categories=category)
            self.fields['size'].queryset = sizes
        else:
            self.fields['size'].queryset = Size.objects.all()
