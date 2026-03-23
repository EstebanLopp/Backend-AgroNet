# Este archivo contiene la lógica de las vistas del carrito de compras.
# Se encarga de recibir las acciones del usuario desde el frontend y ejecutar 
# operaciones sobre el carrito usando la clase Cart.

# Agrega productos al carrito
# Muestra el detalle del carrito
# Elimina productos
# Actualiza cantidades
# Valida disponibilidad y stock antes de modificar el carrito

# Este archivo maneja las vistas del carrito de compras. Recibe las acciones del usuario y 
# valida condiciones como disponibilidad, stock y cantidad antes de modificar el carrito. 
# Además, utiliza mensajes para informar el resultado de cada acción y restringe las operaciones 
# sensibles al método POST, siguiendo buenas prácticas de desarrollo web

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

    if not product.available:
        messages.error(request, "Este producto no está disponible en este momento.")
        return redirect("products:product_detail", slug=product.slug)

    if product.stock <= 0:
        messages.error(request, "Este producto no tiene stock disponible.")
        return redirect("products:product_detail", slug=product.slug)

    current_quantity = 0
    product_id_str = str(product.id)

    if product_id_str in cart.cart:
        current_quantity = cart.cart[product_id_str]["quantity"]

    if current_quantity >= product.stock:
        messages.warning(request, "Ya agregaste la cantidad máxima disponible para este producto.")
        return redirect("cart:cart_detail")

    cart.add(product=product, quantity=1)
    messages.success(request, "Producto agregado al carrito.")
    return redirect("cart:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, "Producto eliminado del carrito.")
    return redirect("cart:cart_detail")

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "La cantidad enviada no es válida.")
        return redirect("cart:cart_detail")

    if not product.available:
        cart.remove(product)
        messages.error(request, "El producto ya no está disponible y fue retirado del carrito.")
        return redirect("cart:cart_detail")

    if product.stock <= 0:
        cart.remove(product)
        messages.error(request, "El producto ya no tiene stock y fue retirado del carrito.")
        return redirect("cart:cart_detail")

    if quantity < 1:
        cart.remove(product)
        messages.info(request, "El producto fue eliminado del carrito.")
        return redirect("cart:cart_detail")

    if quantity > product.stock:
        quantity = product.stock
        messages.warning(request, f"Solo hay {product.stock} unidades disponibles.")

    cart.add(product=product, quantity=quantity, override_quantity=True)
    return redirect("cart:cart_detail")