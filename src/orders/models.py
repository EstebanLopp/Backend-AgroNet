#Este archivo define la estructura de datos del sistema de pedidos, modela tres entidades clave: Order -> pedido principal, OrderItem -> productos dentro del pedido, SellerNotification -> notificaciones para vendedores, ss uno de los archivos más importantes del proyecto porque representa el flujo de compra formalizado en base de datos.

# Almacena pedidos realizados por usuarios, guarda los productos individuales de cada pedido, calcula el total del pedido, relaciona pedidos con vendedores mediante notificaciones, define estados del pedido, métodos de pago y métodos de envío

#Este archivo define los modelos del sistema de pedidos. Order representa el pedido principal del usuario, OrderItem almacena cada producto comprado junto con su precio y cantidad, y SellerNotification permite notificar a las tiendas sobre pedidos relacionados. También incluye reglas de integridad, métodos para calcular subtotales y totales, y estructuras como choices para controlar estados, pagos y envíos.

from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import Store


# Representa el pedido general hecho por un usuario.
class Order(models.Model):
    STATUS_CHOICES = [
        #Estados del pedido
        ("pending", "Pendiente"),
        ("confirmed", "Confirmado"),
        ("prepared", "Preparado"),
        ("shipped", "Enviado"),
        ("delivered", "Entregado"),
        ("cancelled", "Cancelado"),
    ]

    PAYMENT_METHOD_CHOICES = [
        #Métodos de pago
        ("cash", "Efectivo"),
        ("card", "Tarjeta"),
        ("transfer", "Transferencia"),
        ("nequi", "Nequi"),
        ("daviplata", "Daviplata"),
    ]

    SHIPPING_METHOD_CHOICES = [
        #Métodos de envío
        ("standard", "Entrega estándar"),
        ("pickup", "Recoger en tienda"),
        ("express", "Entrega express"),
    ]

    #Relación con el usuario
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created = models.DateTimeField(auto_now_add=True) #->fecha creacion
    updated = models.DateTimeField(auto_now=True) #->fecha actualizacion
    paid = models.BooleanField(default=False) #->indica si el pedido fue pagado

    #estado actual
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    #metodo de pago
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True
    )
    #metodo de envio
    shipping_method = models.CharField(
        max_length=20,
        choices=SHIPPING_METHOD_CHOICES,
        blank=True
    )
    #direccion
    address = models.CharField(
        max_length=255,
        blank=True
    )
    #ciudad
    city = models.CharField(
        max_length=100,
        blank=True
    )
    #observaciones
    notes = models.TextField(
        blank=True
    )
    #Ordena los pedidos del más reciente al más antiguo.
    class Meta:
        ordering = ["-created"]
    #Representación del pedido
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    #Estados del pedido con clases CSS para el frontend
    @property
    def status_badge_class(self):
        return {
            "pending": "pending",
            "confirmed": "confirmed",
            "prepared": "prepared",
            "shipped": "shipped",
            "delivered": "delivered",
            "cancelled": "cancelled",
        }.get(self.status, "pending")

    #Cálculo del total del pedido
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

#Representa cada producto individual dentro de un pedido.
class OrderItem(models.Model):
    #Relación con pedido (Un pedido puede tener muchos items)
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    #Relación con pedidos (Un producto puede aparecer en muchos pedidos)
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2) #->precio producto
    quantity = models.PositiveIntegerField() #->cantidad comprada

    def __str__(self):
        return f"{self.product.name}"
    #Calcula el subtotal de ese producto dentro del pedido.
    def get_cost(self):
        return self.price * self.quantity


#----------------------------------------------------

#Permite generar notificaciones para la tienda asociada a un pedido.
class SellerNotification(models.Model):
    #Relación con tienda (Una tienda puede tener muchas notificaciones)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    #Relación con pedido (Un pedido puede generar notificaciones relacionadas)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="seller_notifications"
    )
    is_read = models.BooleanField(default=False) #->indica si la notificacion fue vista
    created_at = models.DateTimeField(auto_now_add=True)#->fecha de creacion

    class Meta:
        # Ordena notificaciones de más reciente a más antigua.
        ordering = ["-created_at"]
        constraints = [
            #Evita duplicados (Una tienda no puede tener dos notificaciones para el mismo pedido.)
            models.UniqueConstraint(
                fields=["store", "order"],
                name="unique_seller_notification_per_order"
            )
        ]
    #representacion
    def __str__(self):
        return f"Notificación tienda {self.store.name} - pedido #{self.order.id}"
    
    