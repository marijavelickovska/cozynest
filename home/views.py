from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm


def home(request):
    """ A view to return the home page """

    return render(request, 'home/home.html')


def about_us(request):
    """ A view to return the about us page """

    return render(request, 'home/about_us.html')


def our_team(request):
    """ A view to return the our team page """

    return render(request, 'home/our_team.html')


def contact_us(request):
    """
    View for handling Contact Us form submissions.
    Displays the form and saves messages to the database.
    """

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We will get back to you soon.")
            return redirect("contact_us")
    else:
        form = ContactMessageForm()

    return render(request, 'home/contact_us.html', {"form": form})


def careers(request):
    """ A view to return the careers page """

    return render(request, 'home/careers.html')
