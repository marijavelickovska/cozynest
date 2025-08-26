from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal
from django.contrib import messages
from django.conf import settings
import stripe

from .forms import OrderForm
from .models import Order, OrderLineItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.models import BagLineItem
from bag.context_processors import bag_contents


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """
    Handles the checkout process: displays the order form,
    processes submitted orders, creates order line items from the shopping bag,
    updates totals, and initializes Stripe payment intent.
    Redirects to success page on successful order placement.
    """
    bag = bag_contents(request)

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
            order = order_form.save()

            # Add order line items
            for item in bag['bag_items']:
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
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(request, "There was an error with your form. \
                Please double check your information.")
    else:
        bag = bag_contents(request)
        if not bag:
            messages.error(
                request,
                "There's nothing in your bag at the moment"
            )
            return redirect(reverse('products'))

        grand_total = bag.get('grand_total', 0)
        intent = stripe.PaymentIntent.create(
            amount=int(Decimal(grand_total) * 100),
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'postcode': profile.default_postcode,
                    'county': profile.default_county,
                    'country': profile.default_country,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    context = {
        'order_form': order_form,
        'client_secret': intent.client_secret,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts.
    Associates the order with the user profile if logged in, clears the bag,
    optionally saves user info and shows a success message.
    Display the checkout success page.
    """
    order = get_object_or_404(Order, order_number=order_number)
    save_info = request.session.get('save_info')

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()
        BagLineItem.objects.filter(user=request.user).delete()
        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_postcode': order.postcode,
                'default_county': order.county,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
    else:
        if 'bag' in request.session:
            del request.session['bag']

    try:
        send_confirmation_email(order)
    except Exception as e:
        messages.error(request, f"Could not send confirmation email: {e}")

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)


def send_confirmation_email(order):
    """
    Send the user a confirmation email.
    Renders email subject and body templates and sends the email.
    """
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
