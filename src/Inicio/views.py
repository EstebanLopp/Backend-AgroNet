from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from products.models import Product, Category

# Create your views here.

class Inicio(TemplateView):
    template_name = 'pages-general/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 8 productos para "más buscados" (por ahora: más recientes disponibles)
        context["home_products"] = (
            Product.objects.filter(available=True)
            .order_by("-created_at")[:8]
        )

        # 4 categorías visibles en home
        context["home_categories"] = Category.objects.all()[:4]

        return context

class Catalogo(TemplateView):
    template_name = 'pages-general/catalog.html'

class Contacto(TemplateView):
    template_name = 'pages-general/contact.html'

class Producto(TemplateView):
    template_name = 'pages-general/product.html'

class Perfilven(TemplateView):
    template_name = 'pages-general/seller-profile.html'

class QuienesSomos(TemplateView):
    template_name = 'pages-general/whoweare.html'

class Carrito(TemplateView):
    template_name = 'pages-general/cart-general.html'

class InicioSesion(TemplateView):
    template_name = 'pages-general/login.html'

class CrearCuenta(TemplateView):
    template_name = 'pages-general/register_an_account.html'

class ContactoDos(TemplateView):
    template_name = 'pages-general/contact-two.html'

class OlvidasteContraseña(TemplateView):
    template_name = 'pages-general/forgot_password.html'

class TokenOlvidasteContraseña(TemplateView):
    template_name = 'pages-general/token_forgot_password.html'

class ConfirmaContraseña(TemplateView):
    template_name = 'pages-general/confirm_forgot_password.html'








    