# Este archivo configura cómo se visualizan y administran los modelos en el panel de administración de Django (/admin).
# Permite que el administrador del sistema gestione clientes, vendedores y tiendas de forma eficiente.

from django.contrib import admin
from .models import CustomerProfile, SellerProfile, Store


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "document_type", "document_number", "city")
    search_fields = ("user__username", "user__email", "document_number", "phone", "city")

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("is_active", "created_at")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "phone", "city", "created_at")
    search_fields = ("name", "seller__user__username", "seller__user__email", "phone", "city")
    list_filter = ("city", "created_at")