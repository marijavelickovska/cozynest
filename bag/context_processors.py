from decimal import Decimal
from django.conf import settings
from products.models import ProductVariant
from .models import BagLineItem


def bag_contents(request):
    total_quantity = 0
    total_price = Decimal('0.00')

    if request.user.is_authenticated:
        bag_items = BagLineItem.objects.filter(user=request.user)
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
        delivery = (total_price * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)) / Decimal('100')
        amount_remaining_for_free_delivery = settings.FREE_DELIVERY_THRESHOLD - total_price
    else:
        delivery = 0
        amount_remaining_for_free_delivery = 0

    grand_total = delivery + total_price

    context = {
        'bag_items': bag_items,
        'bag_total_quantity': total_quantity,
        'bag_total_price': total_price,
        'delivery': delivery,
        'amount_remaining_for_free_delivery': amount_remaining_for_free_delivery,
        'grand_total': grand_total,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
    }

    return context
