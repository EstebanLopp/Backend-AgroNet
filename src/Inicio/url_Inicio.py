from django.urls import path
from .views import Inicio, Catalogo, Contacto, Producto, Perfilven, QuienesSomos, Carrito, InicioSesion, CrearCuenta, ContactoDos, OlvidasteContraseña, TokenOlvidasteContraseña, ConfirmaContraseña


urlpatterns = [
    path('', Inicio.as_view(), name='index'),
    path('catalog/', Catalogo.as_view(), name='catalog'),
    path('contact/', Contacto.as_view(), name='contact'),
    path('product/<int:id>/', Producto.as_view(), name='product'),
    path('seller-profile/', Perfilven.as_view(), name='seller-profile'),
    path('who-we-are/', QuienesSomos.as_view(), name='who-we-are'),
    path('cart-general/', Carrito.as_view(), name='cart-general'),
    path('login/', InicioSesion.as_view(), name='login'),
    path('register/', CrearCuenta.as_view(), name='register'),
    path('contact-info/', ContactoDos.as_view(), name='contact-info'),
    path('forgot-password/', OlvidasteContraseña.as_view(), name='forgot-password'),
    path('token-forgot-password/', TokenOlvidasteContraseña.as_view(), name='token-forgot-password'),
    path('confirm-password/', ConfirmaContraseña.as_view(), name='confirm-password'),
]