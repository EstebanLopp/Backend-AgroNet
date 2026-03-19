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
]