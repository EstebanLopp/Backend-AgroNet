# Este archivo define las rutas relacionadas con el sistema de contacto.
# Conecta las URLs con las vistas que gestionan el envío y visualización de mensajes.

# Define las rutas del formulario de contacto
# Maneja el flujo de envío y confirmación
# Organiza las URLs bajo el namespace contact

# Este archivo define las rutas del sistema de contacto. Maneja el acceso al formulario, 
# la confirmación del envío y una vista de información adicional. Está organizado con un namespace y 
# sigue un flujo claro de interacción para el usuario, facilitando la navegación y gestión de las 
# solicitudes de contacto.

from django.urls import path
from .views import contact_view, contact_success_view, contact_info_view

app_name = "contact"

urlpatterns = [
    path("contacto/", contact_view, name="contact"),
    path("contacto/enviado/", contact_success_view, name="contact_success"),
    path("contacto/info/", contact_info_view, name="contact_info"),
]