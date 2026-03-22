from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from accounts.models import SellerProfile
from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem, SellerNotification


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

                touched_store_ids = set()

                for item in cart:
                    product = item["product"]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item["price"],
                        quantity=item["quantity"]
                    )

                    touched_store_ids.add(product.store_id)

                    product.stock -= item["quantity"]

                    if product.stock <= 0:
                        product.stock = 0
                        product.status = "disabled"
                        product.available = False

                    product.save()

                for store_id in touched_store_ids:
                    SellerNotification.objects.get_or_create(
                        store_id=store_id,
                        order=order
                    )

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
    return render(request, "orders/success.html")


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


@login_required
def seller_notifications(request):
    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile or not hasattr(seller_profile, "store"):
        messages.error(request, "Primero debes crear una tienda.")
        return redirect("accounts:create_store")

    store = seller_profile.store

    notifications = (
        SellerNotification.objects
        .filter(store=store)
        .select_related("order", "order__user", "store")
        .order_by("-created_at")
    )

    notification_cards = []

    for notification in notifications:
        store_items = (
            notification.order.items
            .filter(product__store=store)
            .select_related("product")
        )

        subtotal = sum(item.get_cost() for item in store_items)
        total_products = sum(item.quantity for item in store_items)

        notification_cards.append({
            "notification": notification,
            "order": notification.order,
            "customer": notification.order.user,
            "items": store_items,
            "subtotal": subtotal,
            "total_products": total_products,
        })

    context = {
        "store": store,
        "notification_cards": notification_cards,
    }

    return render(request, "orders/seller_notifications.html", context)


@login_required
def seller_notification_detail(request, notification_id):
    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile or not hasattr(seller_profile, "store"):
        messages.error(request, "Primero debes crear una tienda.")
        return redirect("accounts:create_store")

    store = seller_profile.store

    notification = get_object_or_404(
        SellerNotification.objects.select_related("order", "order__user", "store"),
        id=notification_id,
        store=store
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    store_items = (
        notification.order.items
        .filter(product__store=store)
        .select_related("product")
    )

    subtotal = sum(item.get_cost() for item in store_items)
    total_products = sum(item.quantity for item in store_items)

    other_notifications = (
        SellerNotification.objects
        .filter(store=store)
        .exclude(id=notification.id)
        .select_related("order", "order__user")
        .order_by("-created_at")[:5]
    )

    context = {
        "store": store,
        "notification": notification,
        "order": notification.order,
        "customer": notification.order.user,
        "items": store_items,
        "subtotal": subtotal,
        "total_products": total_products,
        "other_notifications": other_notifications,
    }

    return render(request, "orders/seller_notification_detail.html", context)


@login_required
def mark_notification_as_read(request, notification_id):
    if request.method != "POST":
        return redirect("orders:seller_notifications")

    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile or not hasattr(seller_profile, "store"):
        messages.error(request, "Primero debes crear una tienda.")
        return redirect("accounts:create_store")

    store = seller_profile.store

    notification = get_object_or_404(
        SellerNotification,
        id=notification_id,
        store=store
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    messages.success(request, "La notificación fue marcada como leída.")
    return redirect("orders:seller_notifications")