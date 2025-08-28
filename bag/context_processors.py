from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from products.models import ProductVariant
from .models import BagLineItem


def bag_contents(request):
    """
    Calculate the contents of the shopping bag.

    Returns a context dictionary containing:
    - list of bag items (with product variant and quantity)
    - total quantity of items
    - total price of items
    - delivery cost
    - amount remaining for free delivery
    - grand total including delivery
    - free delivery threshold

    Handles both authenticated users (database-stored bag)
    and anonymous users (session-stored bag).
    """
    total_quantity = 0
    total_price = Decimal('0.00')

    if request.user.is_authenticated:
        bag_items = BagLineItem.objects.filter(
            user=request.user
        ).order_by('id')
        for item in bag_items:
            total_quantity += item.quantity
            total_price += item.quantity * item.product_variant.price
    else:
        bag = request.session.get('bag', {})
        variant_ids = bag.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        bag_items = []

        for variant in variants:
            quantity = bag.get(str(variant.id), 0)
            total_quantity += quantity
            total_price += quantity * variant.price
            bag_items.append({
                'product_variant': variant,
                'quantity': quantity,
            })

    if total_price < settings.FREE_DELIVERY_THRESHOLD:
        delivery = (
            total_price
            * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
            / Decimal('100')
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        amount_remaining_for_free_delivery = (
            settings.FREE_DELIVERY_THRESHOLD - total_price
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        delivery = Decimal('0.00')
        amount_remaining_for_free_delivery = Decimal('0.00')

    grand_total = (
        total_price + delivery
    ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    context = {
        'bag_items': bag_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'delivery': delivery,
        'amount_remaining_for_free_delivery':
            amount_remaining_for_free_delivery,
        'grand_total': grand_total,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
    }

    return context
