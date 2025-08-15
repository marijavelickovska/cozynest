from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product, ProductVariant
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.context_processors import bag_contents


def checkout(request):
    context = bag_contents(request)

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user_profile = request.user.userprofile
            order.save()

            # Add order line items
            for item in context['bag_items']:
                if request.user.is_authenticated:
                    variant = item.product_variant
                    quantity = item.quantity
                else:
                    variant = item['product_variant']
                    quantity = item['quantity']

                line_item = OrderLineItem(
                    order=order,
                    product_variant=variant,
                    quantity=quantity
                )
                line_item.save()
            
            # Update totals
            order.update_totals()

            messages.success(request, "Order created! Proceed to payment.")
            # return redirect('checkout_success')
        else:
            messages.error(request, "There was an error with your form. \
                Please double check your information.")
    else:
        order_form = OrderForm()

    context = {
        'order_form': order_form
    }

    return render(request, 'checkout/checkout.html', context)
