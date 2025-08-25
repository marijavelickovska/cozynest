from django.contrib import admin
from .models import Size, Color, Category, Product, ProductVariant


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Size model.
    Displays size name and associated categories.
    Allows searching by size name and filtering by categories.
    """
    list_display = ['name', 'get_categories']
    list_filter = ['categories']

    def get_categories(self, obj):
        return ", ".join([c.friendly_name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'


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


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductVariant model.
    Displays product, size, color, price, stock and sku.
    Enables search by product name, size and color.
    Allows filtering by product, size and color.
    """
    list_display = ('product', 'size', 'color', 'price', 'stock')
    search_fields = ('product__name', 'size__name', 'color__name')
    list_filter = ('product', 'size', 'color')
