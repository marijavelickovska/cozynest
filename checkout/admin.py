from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin configuration for the OrderLineItem model.
    Displays line items within an Order in tabular form.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Displays order details, totals, and related line items.
    Allows search, filtering, and read-only order number and totals.
    """

    inlines = (OrderLineItemAdminInline,)

    list_display = (
        'order_number',
        'full_name',
        'email',
        'order_total',
        'delivery_cost',
        'grand_total',
        'date',
    )
    list_filter = ('date', 'delivery_cost', 'grand_total')
    search_fields = ('order_number', 'full_name', 'email')
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
    )

    ordering = ('-date',)
