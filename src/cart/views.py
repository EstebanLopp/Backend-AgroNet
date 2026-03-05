from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib import messages


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.stock < 1:
        messages.error(request, "Este producto está agotado.")
        return redirect("product_list")  

    cart.add(product=product, quantity=1)
    return redirect("cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get("quantity"))
    except (TypeError, ValueError):
        return redirect("cart_detail")

    
    if quantity < 1:
        cart.remove(product)
    elif quantity > product.stock:
        cart.update(product, product.stock)
    else:
        cart.update(product, quantity)

    return redirect("cart_detail")