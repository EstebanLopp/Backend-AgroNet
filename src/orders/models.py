from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("confirmed", "Confirmado"),
        ("shipped", "Enviado"),
        ("delivered", "Entregado"),
        ("cancelled", "Cancelado"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Efectivo"),
        ("card", "Tarjeta"),
        ("transfer", "Transferencia"),
        ("nequi", "Nequi"),
        ("daviplata", "Daviplata"),
    ]

    SHIPPING_METHOD_CHOICES = [
        ("standard", "Entrega estándar"),
        ("pickup", "Recoger en tienda"),
        ("express", "Entrega express"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True
    )
    shipping_method = models.CharField(
        max_length=20,
        choices=SHIPPING_METHOD_CHOICES,
        blank=True
    )
    address = models.CharField(
        max_length=255,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        blank=True
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name}"

    def get_cost(self):
        return self.price * self.quantity
    
    