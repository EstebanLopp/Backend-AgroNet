from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem



@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.paid = True
                order.status = "confirmed"

                for item in cart:
                    product = item["product"]

                    if not product.available:
                        messages.error(
                            request,
                            f'El producto "{product.name}" ya no está disponible.'
                        )
                        return redirect("cart:cart_detail")

                    if item["quantity"] > product.stock:
                        messages.error(
                            request,
                            f'No hay suficiente stock para "{product.name}".'
                        )
                        return redirect("cart:cart_detail")

                order.save()

                for item in cart:
                    product = item["product"]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item["price"],
                        quantity=item["quantity"]
                    )

                    product.stock -= item["quantity"]
                    product.save()

                cart.clear()

                messages.success(request, "Tu pedido fue creado correctamente.")
                return redirect("orders:order_success")
        else:
            messages.error(request, "No se pudo procesar el pedido. Revisa la información ingresada.")

    else:
        initial_data = {}

        if hasattr(request.user, "customer_profile"):
            profile = request.user.customer_profile
            if profile.address:
                initial_data["address"] = profile.address
            if profile.city:
                initial_data["city"] = profile.city

        form = CheckoutForm(initial=initial_data)

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


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