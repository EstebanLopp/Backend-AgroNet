# Este archivo define las rutas del sistema de pedidos. Conecta las URLs con las vistas que manejan el proceso de compra, gestión de pedidos y notificaciones a vendedores.

#Define el flujo de checkout (compra), Permite al usuario ver sus pedidos,Maneja el detalle de pedidos individuales, Gestiona notificaciones para vendedores.

#Este archivo define las rutas del sistema de pedidos. Maneja el flujo de compra desde el checkout hasta la confirmación, permite a los usuarios consultar sus pedidos y a los vendedores gestionar notificaciones relacionadas con ventas. Utiliza rutas dinámicas para acceder a pedidos y notificaciones específicas.

from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order_success"),

    path("mis-pedidos/", views.my_orders, name="my_orders"),
    path("mis-pedidos/<int:order_id>/", views.order_detail, name="order_detail"),

    path("ventas/notificaciones/", views.seller_notifications, name="seller_notifications"),
    path(
        "ventas/notificaciones/<int:notification_id>/",
        views.seller_notification_detail,
        name="seller_notification_detail"
    ),
    path(
        "ventas/notificaciones/<int:notification_id>/leer/",
        views.mark_notification_as_read,
        name="mark_notification_as_read"
    ),
    path(
        "mis-pedidos/<int:order_id>/comprobante-pdf/",
        views.download_order_receipt_pdf,
        name="download_order_receipt_pdf"
    ),
]