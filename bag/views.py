from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import ProductVariant
from .models import BagLineItem


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    """
    Add a product variant to the shopping bag for authenticated or guest users.
    Handles quantity, size, and color selection
    and shows success or error messages.
    """
    if request.method == 'POST':
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))

        try:
            variant = get_object_or_404(
                ProductVariant,
                product_id=product_id,
                size_id=size_id,
                color_id=color_id
            )
        except ProductVariant.DoesNotExist:
            messages.error(
                request,
                "Selected size/color combination is not available."
            )
            return redirect("product_detail", product_id=product_id)

    if request.user.is_authenticated:
        bag_item, created = BagLineItem.objects.get_or_create(
            user=request.user,
            product_variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            bag_item.quantity += quantity
            bag_item.save()

        messages.success(
            request,
            f'Product "{variant.product.name}" has been added to your bag.'
        )
    else:
        bag = request.session.get('bag', {})
        bag[str(variant.id)] = bag.get(str(variant.id), 0) + quantity
        request.session['bag'] = bag

        messages.success(
            request,
            f'Product "{variant.product.name}" has been added to your bag.'
        )

    return redirect('product_detail', product_id=product_id)


def edit_bag_item(request, variant_id):
    """
    Update the quantity of a product variant in the user's bag.
    Handles both authenticated users (database) and anonymous users (session).
    Redirects to the bag view after updating.
    """
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        variant = get_object_or_404(ProductVariant, pk=variant_id)

        if request.user.is_authenticated:
            bag_item = BagLineItem.objects.filter(
                user=request.user,
                product_variant=variant).first()

            if bag_item:
                bag_item.quantity = quantity
                bag_item.save()
        else:
            bag = request.session.get("bag", {})
            if str(variant_id) in bag:
                bag[str(variant_id)] = quantity
                request.session["bag"] = bag

    return redirect("view_bag")


def delete_bag_item(request, variant_id):
    """
    Remove a product variant from the user's bag (session or database)
    and show a success message.
    """
    variant = get_object_or_404(ProductVariant, pk=variant_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            bag_item = BagLineItem.objects.get(
                user=request.user,
                product_variant=variant
            )
            bag_item.delete()
            messages.success(request, f'Product "{variant.product.name}" \
                has been removed from your bag.')
        else:
            bag = request.session.get('bag', {})
            variant_key = str(variant.id)
            if variant_key in bag:
                del bag[variant_key]
                request.session['bag'] = bag
                messages.success(request, f'Product "{variant.product.name}" \
                    has been removed from your bag.')

        return redirect('view_bag')
