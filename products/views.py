from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Size, Color
from .forms import ProductForm, ProductVariantForm
import json


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
            sort = request.GET.get('sort')
            direction = request.GET.get('direction')

            if sort == 'category':
                sortkey = 'category__name'
            elif sort == 'rating':
                sortkey = 'rating'
            elif sort == 'price':
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


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    variants = product.variants.all()
    sizes = product.category.sizes.all() if product.category else Size.objects.none()
    colors = Color.objects.filter(productvariant__product=product).distinct()

    available_sizes = set(v.size_id for v in variants if v.stock > 0)
    available_colors = set(v.color_id for v in variants if v.stock > 0)

    size_color_map = {}
    for variant in variants:
        if variant.stock > 0:
            key = str(variant.size_id)
            size_color_map.setdefault(key, []).append({
                "id": variant.color.id,
                "name": variant.color.name
            })

    context = {
        'product': product,
        'variants': variants,
        'sizes': sizes,
        'colors': colors,
        'available_sizes': available_sizes,
        'available_colors': available_colors,
        'size_color_map_json': json.dumps(size_color_map),
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    template_tab = 'add_product'

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect('add_product')
        else:
            messages.error(request, "Add product failed. Please ensure the form is valid.")
    else:
        form = ProductForm()

    context = {
        'template_tab': template_tab,
        'form': form
    }

    return render(request, 'products/product_managment.html', context)


def get_sizes_for_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sizes = product.category.sizes.all()
    data = [{'id': s.id, 'name': s.name} for s in sizes]
    return JsonResponse({'sizes': data})


def add_product_variant(request):
    template_tab = 'add_product_variant'

    if request.method == "POST":
        form = ProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Variant added successfully")
            return redirect('add_product_variant')
        else:
            messages.error(request, "Add product variant failed. Please ensure the form is valid.")
    else:
        form = ProductVariantForm()

    context = {
        'template_tab': template_tab,
        'form': form
    }

    return render(request, 'products/product_managment.html', context)
