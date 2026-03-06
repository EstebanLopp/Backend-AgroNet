from django.urls import path
from .views import Inicio, Perfilven, QuienesSomos, Carrito, ContactoDos, OlvidasteContraseña, TokenOlvidasteContraseña, ConfirmaContraseña


urlpatterns = [
    path('', Inicio.as_view(), name='index'),
    
    path('seller-profile/', Perfilven.as_view(), name='seller-profile'),
    path('who-we-are/', QuienesSomos.as_view(), name='who-we-are'),
    path('cart-general/', Carrito.as_view(), name='cart-general'),
    path('contact-info/', ContactoDos.as_view(), name='contact-info'),
    path('forgot-password/', OlvidasteContraseña.as_view(), name='forgot-password'),
    path('token-forgot-password/', TokenOlvidasteContraseña.as_view(), name='token-forgot-password'),
    path('confirm-password/', ConfirmaContraseña.as_view(), name='confirm-password'),
]