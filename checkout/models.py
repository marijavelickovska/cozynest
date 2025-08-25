from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.db.models import Sum
from decimal import Decimal
from profiles.models import UserProfile
from products.models import ProductVariant
import uuid


class Order(models.Model):
    """
    Stores all order-related info for a user purchase.
    """
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20, blank=True)
    country = CountryField(blank_label='Country *')
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, blank=True)
    county = models.CharField(max_length=80, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_totals(self):
        """Update order_total and grand_total."""
        self.order_total = self.lineitems.aggregate(
            total=Sum('lineitem_total')
        )['total'] or Decimal('0.00')
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total
                * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
            ) / Decimal('100')
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override save to set order number if not already set."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Individual product line items within an order.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product_variant = models.ForeignKey(
        ProductVariant, null=False, blank=False, on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(
        max_digits=8, decimal_places=2, editable=False
    )

    def save(self, *args, **kwargs):
        """Set the lineitem_total before saving."""
        self.lineitem_total = self.product_variant.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_variant} x {self.quantity}'
