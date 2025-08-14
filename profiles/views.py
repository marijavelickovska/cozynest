from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, UserUpdateForm


@login_required
def profile(request):
    """Display the user's profile with tabs."""
    profile = get_object_or_404(UserProfile, user=request.user)
    tab = request.resolver_match.url_name

    form = None

    if tab == "delivery_information":
        if request.method == "POST":
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Delivery informations updated successfully")
            else:
                messages.error(request, "Update failed. Please ensure the form is valid.")
        else:  # GET request
            form = UserProfileForm(instance=profile)

    if tab == "profile":
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
            else:
                messages.error(request, "Update failed. Please ensure the form is valid.")
        else:  # GET request
            form = UserUpdateForm(instance=profile)

    context = {"form": form, "tab": tab, "on_profile_page": True}
    return render(request, "profiles/profile_base.html", context)
