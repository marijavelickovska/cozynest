from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    products = Product.objects.all()
    query = None
    category = None
    category_obj = None
    current_sorting = request.GET.get('sort', 'None_None')

    if request.GET:
        if 'category' in request.GET:
            category = request.GET.get('category')
            products = products.filter(category__name__iexact=category)

            category_obj = get_object_or_404(Category, name__iexact=category)

        if 'sort' in request.GET:
            sort_full = request.GET.get('sort')
            if '_' in sort_full:
                sort, direction = sort_full.rsplit('_', 1)
            else:
                sort = sort_full
                direction = 'asc'

            if sort == 'category':
                sortkey = 'category__name'
            elif sort == 'rating':
                sortkey = 'rating'
            elif sort == 'base_price':
                sortkey = 'base_price'
            elif sort == 'name':
                sortkey = 'name'
            else:
                sortkey = sort

            if direction == 'desc':
                sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_category': category,
        'category_obj': category_obj,
        'current_sorting': current_sorting
    }

    return render(request, "products/products.html", context)
