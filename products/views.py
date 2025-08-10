from django.shortcuts import render, redirect
from .models import Product


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    products = Product.objects.all()

    category = request.GET.get('category', None)

    if category:
        products = products.filter(category__name__iexact=category)

    sort = request.GET.get("sort", None)
    direction = request.GET.get("direction", None)

    if sort:
        sortkey = sort

        if sort == 'category':
            sortkey = 'category__name'
        elif sort == 'rating':
            sortkey = 'rating'
        elif sort == 'base_price':
            sortkey = 'base_price'

        if direction == "desc":
            sortkey = f"-{sortkey}"

        products = products.order_by(sortkey)

    context = {
        "products": products,
    }

    return render(request, "products/products.html", context)
