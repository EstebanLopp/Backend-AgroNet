from django.urls import path
from .views import Inicio, Catalogo, Contacto, Producto, Perfilven, QuienesSomos, Carrito, InicioSesion, CrearCuenta, ContactoDos, OlvidasteContraseña, TokenOlvidasteContraseña, ConfirmaContraseña, InicioComprador, CatalogoComprador, CarritoComprador, PerfilComprador, EditarCuenta, ContactoComprador, ProductoComprador, ContactoDosComprador, FotoPerfil, ResumenCompra, CrearTienda


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
    path('index-customer/', InicioComprador.as_view(), name='index-customer'),
    path('catalog-customer/', CatalogoComprador.as_view(), name='catalog-customer'),
    path('cart-customer/', CarritoComprador.as_view(), name='cart-customer'),
    path('my_profile/', PerfilComprador.as_view(), name='my_profile'),
    path('edit_account/', EditarCuenta.as_view(), name='edit_account'),
    path('contact-customer/', ContactoComprador.as_view(), name='contact-customer'),
    path('product-customer/', ProductoComprador.as_view(), name='product-customer'),
    path('contact-two-customer/', ContactoDosComprador.as_view(), name='contact-two-customer'),
    path('profile_photo/', FotoPerfil.as_view(), name='profile_photo'),
    path('purchase_summary/', ResumenCompra.as_view(), name='purchase_summary'),
    path('seller_form/', CrearTienda.as_view(), name='seller_form'),
]