from django.shortcuts import render, redirect


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = "All products here"
    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
