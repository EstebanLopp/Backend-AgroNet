from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),

    path("mis-pedidos/", views.my_orders, name="my_orders"),
    path("mis-pedidos/<int:order_id>/", views.order_detail, name="order_detail"),
]