# Este archivo configura cómo se visualizan y gestionan los mensajes de contacto en el panel de 
# administración de Django.

# Registra el modelo ContactMessage en el admin
# Define cómo se muestran los mensajes
# Permite filtrar, buscar y ordenar los registros para facilitar su gestión

# Este archivo configura el panel de administración para gestionar los mensajes de contacto. 
# Permite visualizar información relevante, aplicar filtros, realizar búsquedas y ordenar los registros, 
# facilitando la gestión de las solicitudes enviadas por los usuarios.

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "nombre", "correo", "solicitud", "asunto", "contacto", "is_read")
    list_filter = ("solicitud", "contacto", "is_read", "created_at")
    search_fields = ("nombre", "correo", "identificacion", "telefono", "asunto", "mensaje")
    ordering = ("-created_at",)