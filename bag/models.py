from django.db import models
from django.conf import settings
from products.models import ProductVariant


class BagLineItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_variant')

    def __str__(self):
        return f'{self.product_variant} x {self.quantity}'

    def total_price(self):
        return self.product_variant.price * self.quantity
