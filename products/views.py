from django.db.models import ProtectedError
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, ProductVariant, Category, Size, Color
from .forms import ProductForm, ProductVariantForm
import json


def all_products(request):
    """
    Display all products with optional filtering, sorting, and search.
    """
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
                messages.error(
                    request,
                    "You didn't enter any search criteria!"
                )
                return redirect(reverse('products'))

            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    # pagination
    paginator = Paginator(products, 16)
    page = request.GET.get('page')

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'products': paginated_products,
        'search_term': query,
        'current_category': category,
        'category_obj': category_obj,
        'current_sorting': current_sorting
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """
    A view to show individual product details
    """

    product = get_object_or_404(Product, pk=product_id)
    variants = product.variants.all()
    sizes = (
        product.category.sizes.all()
        if product.category
        else Size.objects.none()
    )
    colors = Color.objects.filter(productvariant__product=product).distinct()

    available_sizes = set(v.size_id for v in variants if v.stock > 0)
    available_colors = set(v.color_id for v in variants if v.stock > 0)

    size_color_map = {}
    for variant in variants:
        if variant.stock > 0:
            key = str(variant.size_id)
            size_color_map.setdefault(key, []).append({
                "id": variant.color.id,
                "name": variant.color.name,
                "stock": variant.stock
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


@login_required
def add_product(request):
    """
    Handle adding a new product via ProductForm.
    """
    template_tab = 'add_product'

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect('add_product')
        else:
            messages.error(
                request,
                "Add product failed. Please ensure the form is valid."
            )
    else:
        form = ProductForm()

    context = {
        'template_tab': template_tab,
        'form': form
    }

    return render(request, 'products/product_managment.html', context)


def get_sizes_for_product(request, product_id):
    """
    Return JSON with sizes for a product's category.
    """
    product = get_object_or_404(Product, pk=product_id)
    sizes = product.category.sizes.all()
    data = [{'id': s.id, 'name': s.name} for s in sizes]
    return JsonResponse({'sizes': data})


@login_required
def add_product_variant(request):
    """
    Handle adding a new product variant via a form
    and display success/error messages.
    """
    template_tab = 'add_product_variant'

    if request.method == "POST":
        form = ProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Variant added successfully")
            return redirect('add_product_variant')
        else:
            messages.error(
                request,
                "Add product variant failed. Please ensure the form is valid."
            )
    else:
        form = ProductVariantForm()

    context = {
        'template_tab': template_tab,
        'form': form
    }

    return render(request, 'products/product_managment.html', context)


@login_required
def edit_product(request, product_id):
    """
    Allow superusers to edit an existing product,
    and show success/error messages.
    """
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit products.")
        return redirect('products')

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('products')
        else:
            messages.error(
                request,
                "Failed to update product. Please check the form."
            )
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'products/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    """
    Allow superusers to delete a product and show a success message.
    """
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete products.")
        return redirect('products')

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('products')

    return redirect(reverse('products'))


@login_required
def all_product_variants(request):
    """
    Display all product variants with related product, size and color info.
    """
    template_tab = 'all_product_variants'

    variants = (
        ProductVariant.objects
        .select_related('product', 'size', 'color')
        .all()
    )
    context = {
        'variants': variants,
        'template_tab': template_tab
    }
    return render(request, 'products/product_managment.html', context)


@login_required
def edit_product_variant(request, variant_id):
    """
    Edit an existing ProductVariant. Displays a form and handles updates.
    """
    variant = get_object_or_404(ProductVariant, pk=variant_id)

    if request.method == 'POST':
        form = ProductVariantForm(
            request.POST,
            request.FILES,
            instance=variant
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Product Variant '{variant.product.name}' updated."
            )
            return redirect('all_product_variants')
        else:
            messages.error(request, "Update failed. Please check the form.")
    else:
        form = ProductVariantForm(instance=variant)

    context = {
        'form': form,
        'variant': variant,
    }
    return render(request, 'products/edit_product_variant.html', context)


@login_required
def delete_product_variant(request, variant_id):
    """
    Deletes a product variant if the user is a superuser.
    Handles protected variants and shows success or error messages.
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            "You are not authorized to delete product variants."
        )
        return redirect('products')

    variant = get_object_or_404(ProductVariant, pk=variant_id)

    if request.method != 'POST':
        return redirect('all_product_variants')

    try:
        variant.delete()
        messages.success(
            request,
            f"Product Variant '{variant.product.name}' deleted successfully."
        )
    except ProtectedError:
        messages.error(
            request,
            ("Cannot delete '"
                f"{variant.product.name}', used in existing orders.")
        )

    return redirect('all_product_variants')
