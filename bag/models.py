from django.db import models
from django.conf import settings
from products.models import ProductVariant


class BagLineItem(models.Model):
    """
    Represents a product variant and quantity added to a user's shopping bag.
    Returns a readable string showing product variant and quantity.
    Returns the total price for this line item (price * quantity).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_variant')

    def __str__(self):
        return f'{self.product_variant} x {self.quantity}'

    def total_price(self):
        return self.product_variant.price * self.quantity
