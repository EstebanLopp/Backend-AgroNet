from django.db import models
from django.utils.text import slugify
from accounts.models import Store


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ("kg", "Kilogramo"),
        ("und", "Unidad"),
        ("lb", "Libra"),
    ]

    STATUS_CHOICES = [
        ("published", "Publicado"),
        ("disabled", "Deshabilitado"),
    ]

    SHIPPING_CHOICES = [
        ("domicilio", "Domicilio"),
        ("recoger", "Recoger en tienda"),
    ]

    WEIGHT_UNIT_CHOICES = [
        ("kg", "Kilogramo"),

    ]

    PAYMENT_CHOICES = [
        ("contra_entrega", "Pago contra entrega"),
        ("consignacion", "Consignación"),
        ("transferencia", "Transferencia"),
    ]

    DELIVERY_TIME_CHOICES = [
        ("24h", "24 horas dentro del municipio"),
        ("48h", "24 a 48 horas"),
        ("3dias", "2 a 3 días hábiles"),
        ("5dias", "3 a 5 días hábiles"),
    ]

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="kg"
    )

    image = models.ImageField(upload_to="products/", blank=False, null=True)
    stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="published"
    )

    shipping_type = models.CharField(
        max_length=20,
        choices=SHIPPING_CHOICES,
        default="domicilio"
    )

    weight_unit = models.CharField(
        max_length=10,
        choices=WEIGHT_UNIT_CHOICES,
        default="kg"
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False
    )

    producer = models.CharField(
        max_length=150,
        verbose_name="Productor o finca",
        null=True,
        blank=True
    )

    delivery_time = models.CharField(
        max_length=20,
        choices=DELIVERY_TIME_CHOICES,
        verbose_name="Entrega estimada",
        default="24h"
    )

    payment_type = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES,
        default="contra_entrega"
    )

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_visible(self):
        return (
            self.available
            and self.status == "published"
            and self.store.is_active
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name