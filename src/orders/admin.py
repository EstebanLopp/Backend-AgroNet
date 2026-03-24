# Este archivo configura el panel de administración para gestionar pedidos (Order), productos dentro de pedidos (OrderItem) y notificaciones a vendedores (SellerNotification).

# Registra modelos del sistema de pedidos en el admin, Permite visualizar pedidos y sus productos asociados, Facilita la gestión de notificaciones para vendedores, Mejora la administración mediante filtros, búsqueda y relaciones.

#Este archivo configura el panel de administración para gestionar pedidos, productos dentro de pedidos y notificaciones a vendedores. Utiliza un TabularInline para mostrar los productos asociados a cada pedido, lo que facilita su gestión. También implementa filtros, búsqueda y uso de relaciones para mejorar la administración de la información.



from django.contrib import admin
from .models import Order, OrderItem, SellerNotification


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created",
        "paid",
        "status",
        "payment_method",
        "shipping_method",
        "city",
    )
    list_filter = ("paid", "status", "payment_method", "shipping_method", "created")
    search_fields = ("id", "user__username", "user__email", "address", "city")
    inlines = [OrderItemInline]

@admin.register(SellerNotification)
class SellerNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "order", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "store")
    search_fields = ("store__name", "order__id", "order__user__username")