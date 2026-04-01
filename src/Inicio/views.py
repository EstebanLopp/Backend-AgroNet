# Este archivo define las vistas de tipo presentación del sistema (frontend) .Se encarga de renderizar templates y, en algunos casos, enviar datos desde la base de datos hacia la interfaz.

# Define vistas basadas en clases (TemplateView), Renderiza páginas estáticas y dinámicas, carga productos y categorías para la página principal, organiza vistas para diferentes tipos de usuario (general y comprador).

# Este archivo define las vistas del módulo inicio utilizando TemplateView. La mayoría de las vistas son estáticas y se encargan de renderizar templates, mientras que la vista principal carga datos dinámicos como productos y categorías desde la base de datos. Esto permite separar la lógica de presentación del resto del sistema.

from django.views.generic import TemplateView # ->renderiza templates sin logica compleja
from products.models import Product, Category # ->modelos usados en la pagina principal

# Create your views here.

class Inicio(TemplateView):
    template_name = 'pages-general/index.html'

    def get_context_data(self, **kwargs): # -> Extiende el contexto del template, Agrega datos dinámicos desde la base de datos
        context = super().get_context_data(**kwargs)

        #Solo productos:disponibles, publicados, de tiendas activas,Ordenados por más recientes, Limita a 8 productos        
        context["home_products"] = (
            Product.objects.filter(available=True, status="published", store__is_active=True, stock__gt=0)
            .order_by("-created_at")[:8]
        )

        #Muestra categorías principales (limita a 4)
        context["home_categories"] = Category.objects.all()[:4]

        return context


#Estas vistas solo renderizan templates, sin lógica adicional

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

class InicioComprador(TemplateView):
    template_name = 'customer-pages/index-customer.html'

class CatalogoComprador(TemplateView):
    template_name = 'customer-pages/catalog-customer.html'

class CarritoComprador(TemplateView):
    template_name = 'customer-pages/cart-customer.html'

class PerfilComprador(TemplateView):
    template_name = 'customer-pages/my_profile.html'

class EditarCuenta(TemplateView):
    template_name = 'customer-pages/edit_account.html'

class ContactoComprador(TemplateView):
    template_name = 'customer-pages/contact-customer.html'

class ProductoComprador(TemplateView):
    template_name = 'customer-pages/product-customer.html'

class ContactoDosComprador(TemplateView):
    template_name = 'customer-pages/contact-two-customer.html'

class FotoPerfil(TemplateView):
    template_name = 'customer-pages/profile_photo.html'

class ResumenCompra(TemplateView):
    template_name = 'customer-pages/purchase_summary.html'

class CrearTienda(TemplateView):
    template_name = 'customer-pages/seller_form.html'



