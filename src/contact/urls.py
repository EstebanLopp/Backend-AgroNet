from django.urls import path
from .views import contact_view, contact_success_view, contact_info_view

app_name = "contact"

urlpatterns = [
    path("contacto/", contact_view, name="contact"),
    path("contacto/enviado/", contact_success_view, name="contact_success"),
    path("contacto/info/", contact_info_view, name="contact_info"),
]