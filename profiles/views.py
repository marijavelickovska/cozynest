from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, UserUpdateForm
from checkout.models import Order


@login_required
def profile(request):
    """
    Display the user's profile with nav tabs.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user
    tab = request.resolver_match.url_name
    form = None
    orders = None

    if tab == "profile":
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
            else:
                messages.error(
                    request, "Update failed. Please ensure the form is valid."
                )
        else:
            form = UserUpdateForm(instance=user)

    if tab == "delivery_information":
        if request.method == "POST":
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Delivery informations updated successfully"
                )
            else:
                messages.error(
                    request, "Update failed. Please ensure the form is valid."
                )
        else:  # GET request
            form = UserProfileForm(instance=profile)

    if tab == "order_history":
        orders = profile.orders.all().order_by('-date')

    context = {
        "form": form,
        "tab": tab,
        "orders": orders,
        "on_profile_page": True}

    return render(request, "profiles/profile_base.html", context)


@login_required
def order_detail(request, order_number):
    """
    Display the details of a specific order for the logged-in user.
    """
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile=request.user.userprofile)

    context = {
        "order": order,
        "tab": "order_history",
    }

    return render(request, "profiles/order_detail.html", context)
