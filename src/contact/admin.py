from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "nombre", "correo", "solicitud", "asunto", "contacto", "is_read")
    list_filter = ("solicitud", "contacto", "is_read", "created_at")
    search_fields = ("nombre", "correo", "identificacion", "telefono", "asunto", "mensaje")
    ordering = ("-created_at",)