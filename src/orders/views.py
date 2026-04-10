#Este archivo contiene la lógica principal del sistema de pedidos. Se encarga de convertir el carrito en una compra real, mostrar el historial de pedidos del cliente y gestionar las notificaciones que reciben los vendedores.

#Procesa el checkout, Crea pedidos y sus items, Descuenta stock de productos Genera notificaciones para tiendas Muestra historial y detalle de pedidos del cliente, Permite a vendedores ver y marcar notificaciones como leídas

#Este archivo contiene la lógica principal del módulo de pedidos. Procesa el checkout validando carrito, stock y formulario, crea el pedido y sus productos asociados, actualiza inventario y genera notificaciones para las tiendas involucradas. Además, permite a los usuarios consultar su historial de compras y a los vendedores gestionar notificaciones relacionadas con ventas. Se aplican buenas prácticas como transacciones atómicas, control de acceso y optimización de consultas.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required #->protege las vistas
from django.db import transaction #->asegura integridad en el checkout
from django.contrib import messages #->informa al usuario lo que ocurrio
from django.conf import settings

from accounts.models import SellerProfile
from cart.cart import Cart #->conecta carrito con el pedido
from .forms import CheckoutForm, OrderStatusUpdateForm
from .models import Order, OrderItem, SellerNotification

import os

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


PDF_MARGIN_X = 16 * mm
PDF_RIGHT_X = 194 * mm
PDF_CONTENT_WIDTH = PDF_RIGHT_X - PDF_MARGIN_X
PDF_PAGE_BG = colors.white
PDF_BRAND_GREEN = colors.HexColor("#22C55E")
PDF_LOGO_BG = colors.HexColor("#22C55E")
PDF_SOFT_GREEN = colors.HexColor("#EAF1EC")
PDF_SOFT_PINK = colors.HexColor("#ECD6EF")
PDF_LINE = colors.HexColor("#D7DED9")
PDF_TEXT_DARK = colors.HexColor("#2E3135")
PDF_TEXT_MUTED = colors.HexColor("#6F757C")
PDF_ROW_ALT = colors.HexColor("#FAFBFA")


def _format_currency(value):
    return f"${float(value):,.2f}"


def _get_pdf_logo_path():
    return os.path.join(settings.BASE_DIR, "static", "assets", "logo-light-transparent.png")


def _normalize_info_line(line):
    text = str(line or "").strip()
    if ":" not in text:
        return ("Detalle", text or "-")

    label, value = text.split(":", 1)
    return (label.strip() or "Detalle", value.strip() or "-")


def _draw_label_chip(pdf, x, y, text, fill_color=PDF_SOFT_GREEN, text_color=PDF_BRAND_GREEN):
    chip_width = max(28 * mm, (len(text) * 2.8 * mm))
    chip_height = 8.5 * mm
    pdf.setFillColor(fill_color)
    pdf.roundRect(x, y - chip_height, chip_width, chip_height, 4 * mm, fill=1, stroke=0)
    pdf.setFillColor(text_color)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawCentredString(x + (chip_width / 2), y - 5.7 * mm, text.upper())
    return chip_width


def _draw_info_entry(pdf, x, y, width, label, value):
    pdf.setFillColor(PDF_TEXT_MUTED)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(x, y, label.upper())
    y -= 5 * mm

    pdf.setFillColor(PDF_TEXT_DARK)
    pdf.setFont("Helvetica", 10)
    for line in _split_text_lines(pdf, value, width, "Helvetica", 10):
        pdf.drawString(x, y, line)
        y -= 4.8 * mm

    return y - 2 * mm


def _split_info_columns(lines):
    entries = [_normalize_info_line(line) for line in lines]
    midpoint = (len(entries) + 1) // 2
    return entries[:midpoint], entries[midpoint:]


def _split_text_lines(pdf, text, max_width, font_name="Helvetica", font_size=10):
    pdf.setFont(font_name, font_size)
    words = str(text or "").split()

    if not words:
        return ["-"]

    lines = []
    current_line = words[0]

    for word in words[1:]:
        candidate = f"{current_line} {word}"
        if pdf.stringWidth(candidate, font_name, font_size) <= max_width:
            current_line = candidate
            continue

        lines.append(current_line)
        current_line = word

    lines.append(current_line)
    return lines


def _draw_wrapped_text(pdf, text, x, y, max_width, line_height, font_name="Helvetica", font_size=10):
    pdf.setFont(font_name, font_size)

    for line in _split_text_lines(pdf, text, max_width, font_name, font_size):
        pdf.drawString(x, y, line)
        y -= line_height

    return y


def _draw_pdf_page_header(pdf, page_number, document_title, heading):
    _, height = A4

    pdf.setFillColor(PDF_PAGE_BG)
    pdf.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    navbar_height = 18 * mm
    navbar_y = height - navbar_height
    pdf.setFillColor(PDF_BRAND_GREEN)
    pdf.rect(0, navbar_y, A4[0], navbar_height, fill=1, stroke=0)

    logo_box_y = height - 35 * mm
    pdf.setFillColor(PDF_LOGO_BG)
    pdf.rect(PDF_MARGIN_X, navbar_y + 1 * mm, 50 * mm, 16 * mm, fill=1, stroke=0)

    logo_path = _get_pdf_logo_path()
    if os.path.exists(logo_path):
        pdf.drawImage(
            ImageReader(logo_path),
            PDF_MARGIN_X + 4 * mm,
            navbar_y + 2.4 * mm,
            width=42 * mm,
            height=13 * mm,
            mask="auto",
            preserveAspectRatio=True,
            anchor="w",
        )

    title_y = height - 46 * mm
    pdf.setFillColor(PDF_TEXT_DARK)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(PDF_MARGIN_X, title_y, "Comprobante")

    pdf.setFillColor(PDF_TEXT_MUTED)
    pdf.setFont("Helvetica", 9.5)
    pdf.drawString(PDF_MARGIN_X, title_y - 7 * mm, document_title)
    pdf.drawString(PDF_MARGIN_X, title_y - 12 * mm, heading)

    pdf.setFillColor(PDF_BRAND_GREEN)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawRightString(PDF_RIGHT_X, title_y - 1 * mm, f"Pagina {page_number}")

    pdf.setFillColor(PDF_TEXT_MUTED)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(PDF_RIGHT_X, title_y - 9 * mm, "AgroNet")

    pdf.setStrokeColor(PDF_LINE)
    pdf.line(PDF_MARGIN_X, title_y - 18 * mm, PDF_RIGHT_X, title_y - 18 * mm)

    return title_y - 28 * mm


def _draw_pdf_info_card(pdf, y, lines):
    left_entries, right_entries = _split_info_columns(lines)
    column_gap = 14 * mm
    column_width = (PDF_CONTENT_WIDTH - column_gap) / 2

    left_x = PDF_MARGIN_X
    right_x = PDF_MARGIN_X + column_width + column_gap
    left_y = y
    right_y = y

    _draw_label_chip(pdf, left_x, left_y, "Cliente")
    _draw_label_chip(pdf, right_x, right_y, "Detalle", fill_color=PDF_SOFT_PINK, text_color=PDF_TEXT_DARK)
    left_y -= 13 * mm
    right_y -= 13 * mm

    for label, value in left_entries:
        left_y = _draw_info_entry(pdf, left_x, left_y, column_width, label, value)

    for label, value in right_entries:
        right_y = _draw_info_entry(pdf, right_x, right_y, column_width, label, value)

    bottom_y = min(left_y, right_y)
    pdf.setStrokeColor(PDF_LINE)
    pdf.line(PDF_MARGIN_X, bottom_y, PDF_RIGHT_X, bottom_y)
    return bottom_y - 8 * mm


def _draw_pdf_table_header(pdf, y):
    pdf.setFillColor(PDF_TEXT_DARK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(PDF_MARGIN_X, y, "SERVICIO")
    pdf.drawRightString(126 * mm, y, "CANTIDAD")
    pdf.drawRightString(156 * mm, y, "PRECIO")
    pdf.drawRightString(PDF_RIGHT_X, y, "TOTAL")

    pdf.setStrokeColor(PDF_LINE)
    pdf.line(PDF_MARGIN_X, y - 4 * mm, PDF_RIGHT_X, y - 4 * mm)
    return y - 10 * mm


def _get_pdf_item_row_height(pdf, item):
    product_lines = _split_text_lines(pdf, item.product.name, 86 * mm, "Helvetica", 10)
    return max(10 * mm, (len(product_lines) * 5.2 * mm) + 3 * mm), product_lines


def _draw_pdf_item_row(pdf, y, item, row_index):
    row_height, product_lines = _get_pdf_item_row_height(pdf, item)
    row_bottom = y - row_height + 2 * mm

    if row_index % 2 == 1:
        pdf.setFillColor(PDF_ROW_ALT)
        pdf.rect(PDF_MARGIN_X, row_bottom - 1 * mm, PDF_CONTENT_WIDTH, row_height, fill=1, stroke=0)

    text_y = y - 1.5 * mm
    pdf.setFillColor(PDF_TEXT_DARK)
    pdf.setFont("Helvetica", 10)
    for line in product_lines:
        pdf.drawString(PDF_MARGIN_X, text_y, line)
        text_y -= 5 * mm

    center_y = y - (row_height / 2) + 1.5 * mm
    pdf.setFont("Helvetica", 9)
    pdf.drawRightString(126 * mm, center_y, str(item.quantity))
    pdf.drawRightString(156 * mm, center_y, _format_currency(item.price))
    pdf.drawRightString(PDF_RIGHT_X, center_y, _format_currency(item.get_cost()))

    pdf.setStrokeColor(PDF_LINE)
    pdf.line(PDF_MARGIN_X, row_bottom - 2 * mm, PDF_RIGHT_X, row_bottom - 2 * mm)

    return row_bottom - 5 * mm


def _draw_pdf_total_box(pdf, y, total_text):
    left_x = PDF_MARGIN_X
    right_x = 138 * mm
    total_value = total_text.split(":", 1)[-1].strip() if ":" in total_text else total_text

    _draw_label_chip(pdf, left_x, y, "Datos de pago", fill_color=PDF_SOFT_PINK, text_color=PDF_TEXT_DARK)

    pdf.setFillColor(PDF_TEXT_MUTED)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(left_x, y - 14 * mm, "Pago registrado en la plataforma")
    pdf.drawString(left_x, y - 18.8 * mm, "Consulta el estado del pedido para")
    pdf.drawString(left_x, y - 23.6 * mm, "hacer seguimiento al envio.")

    pdf.setFillColor(PDF_TEXT_MUTED)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(right_x, y - 8 * mm, "Subtotal")
    pdf.drawRightString(PDF_RIGHT_X, y - 8 * mm, total_value)

    pdf.setStrokeColor(PDF_LINE)
    pdf.line(right_x, y - 12 * mm, PDF_RIGHT_X, y - 12 * mm)

    pdf.setFillColor(PDF_TEXT_DARK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(right_x, y - 19 * mm, "Total")
    pdf.drawRightString(PDF_RIGHT_X, y - 19 * mm, total_value)

    return y - 30 * mm


def _draw_pdf_footer(pdf, footer_text):
    pdf.setStrokeColor(PDF_LINE)
    pdf.line(PDF_MARGIN_X, 20 * mm, PDF_RIGHT_X, 20 * mm)

    pdf.setFillColor(PDF_TEXT_MUTED)
    pdf.setFont("Helvetica", 8)
    _draw_wrapped_text(pdf, footer_text, PDF_MARGIN_X, 15.5 * mm, 132 * mm, 4 * mm, font_size=8)

    pdf.setFillColor(PDF_BRAND_GREEN)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawRightString(PDF_RIGHT_X, 15.5 * mm, "Sistema de pedidos")


def _start_pdf_page(pdf, document_title, heading):
    page_number = pdf.getPageNumber()
    return _draw_pdf_page_header(pdf, page_number, document_title, heading)


def _build_order_pdf(response, *, document_title, heading, lines, items, total_text, footer_text):
    pdf = canvas.Canvas(response, pagesize=A4)
    _, height = A4

    pdf.setTitle(document_title)
    y = _start_pdf_page(pdf, document_title, heading)
    y = _draw_pdf_info_card(pdf, y, lines)
    y = _draw_pdf_table_header(pdf, y)

    for row_index, item in enumerate(items):
        row_height, _ = _get_pdf_item_row_height(pdf, item)
        if y - row_height < 28 * mm:
            _draw_pdf_footer(pdf, footer_text)
            pdf.showPage()
            y = _start_pdf_page(pdf, document_title, heading)
            y = _draw_pdf_info_card(pdf, y, lines)
            y = _draw_pdf_table_header(pdf, y)

        y = _draw_pdf_item_row(pdf, y, item, row_index)

    y = _draw_pdf_total_box(pdf, y, total_text)
    _draw_pdf_footer(pdf, footer_text)

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
        total_text=f"Total: {_format_currency(order.get_total_price())}",
        footer_text="Comprobante generado automaticamente para consulta del cliente."
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
        total_text=f"Total tienda: {_format_currency(subtotal)}",
        footer_text="Detalle generado automaticamente para la tienda receptora del pedido."
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