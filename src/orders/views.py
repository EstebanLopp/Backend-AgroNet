#Este archivo contiene la lógica principal del sistema de pedidos. Se encarga de convertir el carrito en una compra real, mostrar el historial de pedidos del cliente y gestionar las notificaciones que reciben los vendedores.

#Procesa el checkout, Crea pedidos y sus items, Descuenta stock de productos Genera notificaciones para tiendas Muestra historial y detalle de pedidos del cliente, Permite a vendedores ver y marcar notificaciones como leídas

#Este archivo contiene la lógica principal del módulo de pedidos. Procesa el checkout validando carrito, stock y formulario, crea el pedido y sus productos asociados, actualiza inventario y genera notificaciones para las tiendas involucradas. Además, permite a los usuarios consultar su historial de compras y a los vendedores gestionar notificaciones relacionadas con ventas. Se aplican buenas prácticas como transacciones atómicas, control de acceso y optimización de consultas.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required #->protege las vistas
from django.db import transaction #->asegura integridad en el checkout
from django.contrib import messages #->informa al usuario lo que ocurrio

from accounts.models import SellerProfile
from cart.cart import Cart #->conecta carrito con el pedido
from .forms import CheckoutForm, OrderStatusUpdateForm
from .models import Order, OrderItem, SellerNotification

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def _draw_wrapped_text(pdf, text, x, y, max_width, line_height, font_name="Helvetica", font_size=10):
    pdf.setFont(font_name, font_size)
    words = str(text or "").split()

    if not words:
        pdf.drawString(x, y, "-")
        return y - line_height

    current_line = words[0]

    for word in words[1:]:
        candidate = f"{current_line} {word}"
        if pdf.stringWidth(candidate, font_name, font_size) <= max_width:
            current_line = candidate
            continue

        pdf.drawString(x, y, current_line)
        y -= line_height
        current_line = word

    pdf.drawString(x, y, current_line)
    return y - line_height


def _draw_pdf_table_header(pdf, y):
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(20 * mm, y, "Producto")
    pdf.drawString(105 * mm, y, "Cant.")
    pdf.drawString(125 * mm, y, "Precio")
    pdf.drawString(160 * mm, y, "Subtotal")
    y -= 5 * mm
    pdf.line(20 * mm, y, 190 * mm, y)
    return y - 8 * mm


def _build_order_pdf(response, *, document_title, heading, lines, items, total_text, footer_text):
    pdf = canvas.Canvas(response, pagesize=A4)
    _, height = A4
    y = height - 30 * mm

    pdf.setTitle(document_title)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(20 * mm, y, "AgroNet")
    y -= 10 * mm

    pdf.setFont("Helvetica", 10)
    pdf.drawString(20 * mm, y, heading)
    y -= 8 * mm

    for line in lines:
        y = _draw_wrapped_text(pdf, line, 20 * mm, y, 165 * mm, 6 * mm)

    y -= 4 * mm
    y = _draw_pdf_table_header(pdf, y)
    pdf.setFont("Helvetica", 10)

    for item in items:
        if y < 25 * mm:
            pdf.showPage()
            y = height - 30 * mm
            y = _draw_pdf_table_header(pdf, y)
            pdf.setFont("Helvetica", 10)

        product_name = item.product.name[:40]
        pdf.drawString(20 * mm, y, product_name)
        pdf.drawString(105 * mm, y, str(item.quantity))
        pdf.drawString(125 * mm, y, f"${item.price}")
        pdf.drawString(160 * mm, y, f"${item.get_cost()}")
        y -= 7 * mm

    y -= 5 * mm
    pdf.line(20 * mm, y, 190 * mm, y)
    y -= 10 * mm

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(120 * mm, y, total_text)
    y -= 12 * mm

    pdf.setFont("Helvetica", 9)
    _draw_wrapped_text(pdf, footer_text, 20 * mm, y, 170 * mm, 5 * mm, font_size=9)

    pdf.save()
    return response


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
                #crea el pedido sin guardarlo aún, lo asocia al usuario autenticado, marca el pedido como pagado y usa el estado inicial por defecto del modelo
                order = form.save(commit=False)
                order.user = request.user
                order.paid = True

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

@login_required
def download_order_receipt_pdf(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="comprobante_pedido_{order.id}.pdf"'

    customer_name = request.user.get_full_name() or request.user.username
    payment_method = order.get_payment_method_display() if order.payment_method else "No especificado"
    shipping_method = order.get_shipping_method_display() if order.shipping_method else "No especificado"
    address = f"{order.address}, {order.city}" if order.address else "No especificada"
    return _build_order_pdf(
        response,
        document_title=f"Comprobante Pedido #{order.id}",
        heading=f"Comprobante de compra - Pedido #{order.id}",
        lines=[
            f"Cliente: {customer_name}",
            f"Fecha: {order.created.strftime('%d/%m/%Y %H:%M')}",
            f"Estado: {order.get_status_display()}",
            f"Método de pago: {payment_method}",
            f"Método de envío: {shipping_method}",
            f"Dirección: {address}",
        ],
        items=order.items.all(),
        total_text=f"Total: ${order.get_total_price()}",
        footer_text="Documento generado por AgroNet como comprobante interno de compra."
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
#marca la notificación como leída automáticamente
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

    if request.method == "POST":
        previous_status = notification.order.status
        status_form = OrderStatusUpdateForm(request.POST, instance=notification.order)

        if status_form.is_valid():
            order = status_form.save()

            if not notification.is_read:
                notification.is_read = True
                notification.save(update_fields=["is_read"])

            if order.status != previous_status:
                messages.success(request, "El estado del pedido ha sido actualizado con exito.")
            else:
                messages.info(request, "El pedido ya tenía ese estado.")

            return redirect("orders:seller_notification_detail", notification_id=notification.id)

        messages.error(request, "No se pudo actualizar el estado del pedido.")
    else:
        status_form = OrderStatusUpdateForm(instance=notification.order)

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
        "status_form": status_form,
    }

    return render(request, "orders/seller_notification_detail.html", context)


@login_required
def download_seller_notification_pdf(request, notification_id):
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

    store_items = (
        notification.order.items
        .filter(product__store=store)
        .select_related("product")
    )
    subtotal = sum(item.get_cost() for item in store_items)
    customer_name = notification.order.user.get_full_name() or notification.order.user.username
    payment_method = (
        notification.order.get_payment_method_display()
        if notification.order.payment_method else "No especificado"
    )
    shipping_method = (
        notification.order.get_shipping_method_display()
        if notification.order.shipping_method else "No especificado"
    )
    address = (
        f"{notification.order.address}, {notification.order.city}"
        if notification.order.address else "No especificada"
    )
    notes = notification.order.notes or "Sin notas."

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="detalle_venta_pedido_{notification.order.id}_tienda_{store.id}.pdf"'
    )

    return _build_order_pdf(
        response,
        document_title=f"Detalle Venta Pedido #{notification.order.id}",
        heading=f"Detalle del pedido recibido - Pedido #{notification.order.id}",
        lines=[
            f"Tienda: {store.name}",
            f"Comprador: {customer_name}",
            f"Fecha: {notification.order.created.strftime('%d/%m/%Y %H:%M')}",
            f"Estado general: {notification.order.get_status_display()}",
            f"Método de pago: {payment_method}",
            f"Método de envío: {shipping_method}",
            f"Dirección: {address}",
            f"Notas: {notes}",
        ],
        items=store_items,
        total_text=f"Total tienda: ${subtotal}",
        footer_text="Documento generado por AgroNet con el detalle del pedido para la tienda receptora."
    )


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