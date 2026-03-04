from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart.cart import Cart
from .models import Order, OrderItem
from django.contrib import messages


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('cart_detail')

    if request.method == "POST":
        with transaction.atomic():

            order = Order.objects.create(user=request.user)

            for item in cart:
                product = item['product']

                # Validación de stock
                if item['quantity'] > product.stock:
                    return redirect('cart_detail')

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )

                product = item['product']
                product.stock -= item['quantity']
                product.save()

            cart.clear()

        return redirect('orders:order_success')

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_success(request):
    return render(request, 'orders/success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "orders/my_orders.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user
    )
    return render(request, "orders/order_detail.html", {"order": order})