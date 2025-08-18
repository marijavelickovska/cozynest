from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal
from django.contrib import messages
from django.conf import settings
import stripe

from .forms import OrderForm
from .models import Order, OrderLineItem
from bag.models import BagLineItem
from bag.context_processors import bag_contents


stripe.api_key = settings.STRIPE_SECRET_KEY


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

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. \
                Please double check your information.")
    else:
        order_form = OrderForm()

        context = bag_contents(request)
        grand_total = context.get('grand_total', 0)
        intent = stripe.PaymentIntent.create(
            amount=int(Decimal(grand_total) * 100),
            currency=settings.STRIPE_CURRENCY,
        )

    context = {
        'order_form': order_form,
        'client_secret': intent.client_secret,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        BagLineItem.objects.filter(user=request.user).delete()
    else:
        if 'bag' in request.session:
            del request.session['bag']
            request.session.modified = True

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)


def send_confirmation_email(order):
    """Send the user a confirmation email"""
    cust_email = order.email
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order})
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
