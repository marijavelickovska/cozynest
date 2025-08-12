from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductVariant
from .models import BagLineItem


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    if request.method == 'POST':
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))
        variant = get_object_or_404(
            ProductVariant,
            product_id=product_id,
            size_id=size_id,
            color_id=color_id
        )

    if request.user.is_authenticated:
        bag_item, created = BagLineItem.objects.get_or_create(
            user=request.user,
            product_variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            bag_item.quantity += quantity
            bag_item.save()
    else:
        bag = request.session.get('bag', {})
        bag[str(variant.id)] = bag.get(str(variant.id), 0) + quantity
        request.session['bag'] = bag

        messages.success(request, f'Product "{variant.product.name}" has been added to your bag.')
        return redirect('view_bag')

    return redirect('product_detail', product_id=product_id)
