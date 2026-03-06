from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from cart.cart import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('cart_detail')

    if request.method == "POST":
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                paid=True,
                status="confirmed",
                payment_method="nequi",
                shipping_method="standard",
                address="Dirección pendiente",
                city="Cali",
                notes="Pedido generado desde simulación de compra",
            )

            for item in cart:
                product = item['product']

                # Validación de stock
                if item['quantity'] > product.stock:
                    messages.error(
                        request,
                        f"No hay suficiente stock para {product.name}. Disponible: {product.stock}."
                    )
                    return redirect('cart_detail')

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )

                product.stock -= item['quantity']
                product.save()

            cart.clear()

        messages.success(request, "Pedido realizado con éxito.")
        return redirect('orders:order_success')

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_success(request):
    return render(request, 'orders/success.html')


@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
    )
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user
    )

    other_orders = (
        Order.objects
        .filter(user=request.user)
        .exclude(id=order.id)
        .only(
            "id",
            "created",
            "paid",
            "status",
            "payment_method",
            "shipping_method",
            "address",
            "city",
            "notes",
        )[:3]
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "other_orders": other_orders,
        }
    )