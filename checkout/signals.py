from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem


@receiver(pre_save, sender=OrderLineItem)
def store_old_quantity(sender, instance, **kwargs):
    """
    Store old quantity before updating so we can adjust stock correctly.
    """
    if instance.pk:
        try:
            old_item = OrderLineItem.objects.get(pk=instance.pk)
            instance._old_quantity = old_item.quantity
        except OrderLineItem.DoesNotExist:
            instance._old_quantity = None
    else:
        instance._old_quantity = None


@receiver(post_save, sender=OrderLineItem)
def update_order_on_save(sender, instance, created, **kwargs):
    """
    Update order totals and adjust stock
    when a line item is created or updated.
    """
    # Update totals after save
    instance.order.update_totals()

    # Adjust stock
    if created:
        instance.product_variant.reduce_stock(instance.quantity)
    else:
        if instance._old_quantity is not None:
            diff = instance.quantity - instance._old_quantity
            if diff > 0:
                instance.product_variant.reduce_stock(diff)
            elif diff < 0:
                instance.product_variant.restore_stock(abs(diff))


@receiver(post_delete, sender=OrderLineItem)
def update_order_on_delete(sender, instance, **kwargs):
    """
    Restore stock and update totals when a line item is deleted.
    """
    instance.product_variant.restore_stock(instance.quantity)
    instance.order.update_totals()
