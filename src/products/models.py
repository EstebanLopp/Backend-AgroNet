#Este archivo define la estructura de datos del catálogo del sistema. Modela dos entidades principales: Category -> categorías de productos, Product -> productos que venden las tiendas, Este archivo es central porque conecta directamente con: página de inicio, catálogo, carrito, pedidos, tiendas

#Define categorías para clasificar productos, define la estructura completa de cada producto, relaciona productos con tiendas y categorías, controla visibilidad y disponibilidad, genera slugs automáticamente para URLs amigables

#Este archivo define los modelos del catálogo del sistema. Category organiza los productos por categorías, y Product almacena toda la información comercial, logística y de inventario de cada producto. Además, implementa relaciones con tiendas y categorías, control de visibilidad y generación automática de slugs únicos para URLs amigables.

from django.db import models
from django.utils.text import slugify
from accounts.models import Store

#representa una categoría del catálogo
class Category(models.Model):
    #campos principales (name -> nombre de la categoría, slug -> versión amigable para UR, unique=True -> evita duplicados)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    #Personaliza cómo se muestra el nombre en el admin
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    #representacion
    def __str__(self):
        return self.name

#Representa cada producto que una tienda publica en el sistema.
class Product(models.Model):
    UNIT_CHOICES = [
        ("kg", "Kilogramo"),
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
        ("g", "Gramo"),
        ("lb", "Libra"),
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

    #relacion con la tienda (Una tienda puede tener muchos productos, Cada producto pertenece a una tienda)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products"
    )
    #relacion con categoria (Una categoría puede tener muchos productos, Cada producto pertenece a una categoría)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    #campos principales de producto
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
        #Muestra los productos más recientes primero
        ordering = ["-created_at"]

    #Determina si el producto debe mostrarse al usuario. Un producto es visible solo si: está disponible, está publicado y su tienda está activa
    @property
    def is_visible(self):
        return (
            self.available
            and self.status == "published"
            and self.store.is_active
        )

    #Si el producto no tiene slug: genera uno con slugify(self.name), verifica si ya existe, si existe, agrega contador: producto, producto-1, producto-2
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