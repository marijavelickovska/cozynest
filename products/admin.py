from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Size, Color, Category, Product, ProductVariant


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Size model.
    Displays size name and allows search and filtering by name.
    """
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Color model.
    Displays color name and hex code, allows search and filtering.
    """
    list_display = ('name', 'hex_code')
    search_fields = ('name', 'hex_code')
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    Displays name and friendly name, allows searching and filtering.
    """
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    Displays product details including name, category,
    base price and timestamps.
    Enables search by name and category,
    and filtering by category and creation date.
    """
    list_display = (
        'name', 'category', 'base_price', 'created_on', 'updated_on'
    )
    search_fields = ('name', 'category__name', 'description')
    list_filter = ('category', 'created_on')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductVariant model.
    Displays product, size, color, price, stock and sku.
    Enables search by product name, sku, size and color.
    Allows filtering by product, size and color.
    """
    list_display = ('product', 'size', 'color', 'price', 'stock', 'sku')
    search_fields = ('product__name', 'sku', 'size__name', 'color__name')
    list_filter = ('product', 'size', 'color')
