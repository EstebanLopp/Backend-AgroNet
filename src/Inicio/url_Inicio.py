# Este archivo define las rutas principales del sistema relacionadas con páginas generales (vistas públicas).Actúa como punto de entrada para varias vistas informativas y de navegación.

# sirve para definir rutas para páginas generales del sistema, Usa vistas basadas en clases y Maneja la navegación principal del usuario

# Este archivo define las rutas principales del sistema, utiliza vistas basadas en clases para organizar la lógica de presentación y permite gestionar la navegación del usuario entre secciones como inicio, información, carrito y recuperación de contraseña.


from django.urls import path
#Importa vistas basadas en clases, cada vista representa una página del sistema
from .views import Inicio, Perfilven, QuienesSomos, Carrito, ContactoDos, OlvidasteContraseña, TokenOlvidasteContraseña, ConfirmaContraseña, CrearTienda


urlpatterns = [
    path('', Inicio.as_view(), name='index'),
    
    path('seller-profile/', Perfilven.as_view(), name='seller-profile'),
    path('who-we-are/', QuienesSomos.as_view(), name='who-we-are'),
    path('cart-general/', Carrito.as_view(), name='cart-general'),
    path('contact-info/', ContactoDos.as_view(), name='contact-info'),
    path('forgot-password/', OlvidasteContraseña.as_view(), name='forgot-password'),
    path('token-forgot-password/', TokenOlvidasteContraseña.as_view(), name='token-forgot-password'),
    path('confirm-password/', ConfirmaContraseña.as_view(), name='confirm-password'),
    path('crear-tienda/', CrearTienda.as_view(), name='create_store'),
]