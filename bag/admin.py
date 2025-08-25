from django.contrib import admin
from .models import BagLineItem


@admin.register(BagLineItem)
class BagLineItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for BagLineItem model.
    Shows user, product variant, quantity and added date.
    Enables searching by user and product variant.
    """
    list_display = ('user', 'product_variant', 'quantity', 'added_on')
    search_fields = (
        'user__username',
        'product_variant__product__name',
        'product_variant__color__name',
        'product_variant__size__name'
    )
    list_filter = ('added_on',)
