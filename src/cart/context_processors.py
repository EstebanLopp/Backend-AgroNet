# Este archivo define un context processor que permite que el carrito esté 
# disponible en todos los templates del sistema automáticamente.

# Crea una instancia del carrito (Cart)
# La inyecta en el contexto global de Django
# Permite acceder al carrito desde cualquier template sin pasarlo manualmente desde las vistas

# Este archivo define un context processor que hace disponible el carrito en todos los templates del 
# sistema. Esto evita tener que pasar el carrito manualmente desde cada vista y permite acceder a él de 
# forma global, mejorando la organización y reutilización del código

from .cart import Cart

def cart(request):
    return {"cart": Cart(request)}