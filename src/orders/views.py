#Este archivo contiene la lógica principal del sistema de pedidos. Se encarga de convertir el carrito en una compra real, mostrar el historial de pedidos del cliente y gestionar las notificaciones que reciben los vendedores.

#Procesa el checkout, Crea pedidos y sus items, Descuenta stock de productos Genera notificaciones para tiendas Muestra historial y detalle de pedidos del cliente, Permite a vendedores ver y marcar notificaciones como leídas

#Este archivo contiene la lógica principal del módulo de pedidos. Procesa el checkout validando carrito, stock y formulario, crea el pedido y sus productos asociados, actualiza inventario y genera notificaciones para las tiendas involucradas. Además, permite a los usuarios consultar su historial de compras y a los vendedores gestionar notificaciones relacionadas con ventas. Se aplican buenas prácticas como transacciones atómicas, control de acceso y optimización de consultas.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required #->protege las vistas
from django.db import transaction #->asegura integridad en el checkout
from django.contrib import messages #->informa al usuario lo que ocurrio

from accounts.models import SellerProfile
from cart.cart import Cart #->conecta carrito con el pedido
from .forms import CheckoutForm
from .models import Order, OrderItem, SellerNotification


#Toma los productos del carrito y los convierte en un pedido formal.
@login_required
def checkout(request):
    cart = Cart(request)
    #Si el carrito no tiene productos, no se puede comprar
    if len(cart) == 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("cart:cart_detail")

    if request.method == "POST":
        #Si el formulario es válido, entra al flujo principal de creación del pedido.
        form = CheckoutForm(request.POST)

        if form.is_valid():
            #Garantiza que todo el proceso se haga completo o no se haga nada:si falla la creación de items,si falla actualización de stock,si falla alguna parte crítica entonces la operación se revierte y no quedan datos inconsistentes.
            with transaction.atomic():
                #crea el pedido sin guardarlo aún, lo asocia al usuario autenticado, marca el pedido como pagado, establece estado inicial en confirmado
                order = form.save(commit=False)
                order.user = request.user
                order.paid = True
                order.status = "confirmed"

                #valida que el producto siga disponible, que haya stock suficiente
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
                #guardado del pedido
                order.save()

                touched_store_ids = set()

                for item in cart:
                    product = item["product"]
                    #crea cada línea del pedido,guarda el precio histórico del producto,guarda cantidad comprada
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item["price"],
                        quantity=item["quantity"]
                    )

                    touched_store_ids.add(product.store_id)
                    #descuenta stock real, si el producto se agota:lo deja en 0, lo deshabilita, lo marca como no disponible
                    product.stock -= item["quantity"]

                    if product.stock <= 0:
                        product.stock = 0
                        product.status = "disabled"
                        product.available = False

                    product.save()
                #crea una notificación por tienda involucrada, usa get_or_create para no duplicar registros
                for store_id in touched_store_ids:
                    SellerNotification.objects.get_or_create(
                        store_id=store_id,
                        order=order
                    )

                #limpieza del carrito
                cart.clear()

                messages.success(request, "Tu pedido fue creado correctamente.")
                return redirect("orders:order_success")
        else:
            messages.error(request, "No se pudo procesar el pedido. Revisa la información ingresada.")

    else:
        initial_data = {}
        #si el usuario ya tiene perfil con dirección y ciudad precarga esos datos en el formulario
        if hasattr(request.user, "customer_profile"):
            profile = request.user.customer_profile
            if profile.address:
                initial_data["address"] = profile.address
            if profile.city:
                initial_data["city"] = profile.city

        form = CheckoutForm(initial=initial_data)

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})

#compra exitosa (renderiza la vista de confirmación de compra)
@login_required
def order_success(request):
    return render(request, "orders/success.html")

#historial de pedidos (obtiene los pedidos del usuario autenticado)
@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        #optimiza consultas trayendo items y productos relacionados.
        .prefetch_related("items__product")
    )
    return render(request, "orders/my_orders.html", {"orders": orders})

#obtiene un pedido específico del usuario, evita que un usuario vea pedidos de otro, también carga otros pedidos del mismo usuario como referencia
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user
    )
    #trae solo los campos necesarios para other_orders.
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

#verifica si el usuario tiene perfil de vendedor y tienda, obtiene notificaciones de esa tienda, construye tarjetas informativas para mostrar en la interfaz
@login_required
def seller_notifications(request):
    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile or not hasattr(seller_profile, "store"):
        messages.error(request, "Primero debes crear una tienda.")
        return redirect("accounts:create_store")

    store = seller_profile.store

    notifications = (
        #trae notificación, pedido, usuario y tienda relacionados en una sola estrategia optimizada.
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
        #Construcción de tarjetas
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


#muestra detalle completo de una notificación, obtiene solo los items de esa tienda dentro del pedido
marca la notificación como leída automáticamente
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

    #cambia solo el campo necesario
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    #si un pedido tiene productos de varias tiendas, el vendedor solo ve los suyos.
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


#solo permite operación si existe tienda y notificación válida, marca manualmente como leída, exige método POST indirectamente mediante validación manual
@login_required
def mark_notification_as_read(request, notification_id):
    #Restricción de método
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