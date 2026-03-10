from django.views.generic import TemplateView
from products.models import Product, Category

# Create your views here.

class Inicio(TemplateView):
    template_name = 'pages-general/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        context["home_products"] = (
            Product.objects.filter(available=True)
            .order_by("-created_at")[:8]
        )

        
        context["home_categories"] = Category.objects.all()[:4]

        return context


class Perfilven(TemplateView):
    template_name = 'pages-general/seller-profile.html'

class QuienesSomos(TemplateView):
    template_name = 'pages-general/whoweare.html'

class Carrito(TemplateView):
    template_name = 'pages-general/cart-general.html'

class ContactoDos(TemplateView):
    template_name = 'pages-general/contact-two.html'

class OlvidasteContraseña(TemplateView):
    template_name = 'pages-general/forgot_password.html'

class TokenOlvidasteContraseña(TemplateView):
    template_name = 'pages-general/token_forgot_password.html'

class ConfirmaContraseña(TemplateView):
    template_name = 'pages-general/confirm_forgot_password.html'








    