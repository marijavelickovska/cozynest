from django.shortcuts import render


def home(request):
    """ A view to return the home page """

    return render(request, 'home/home.html')


def about_us(request):
    """ A view to return the about us page """

    return render(request, 'home/about_us.html')


def contact_us(request):
    """ A view to return the contact us page """

    return render(request, 'home/contact_us.html')
