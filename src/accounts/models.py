# Este archivo define la estructura de la base de datos para la aplicación accounts.
# Aquí se modelan las entidades principales del sistema:

# Perfil de cliente
# Perfil de vendedor
# Tienda

# Extiende el modelo User de Django con información adicional
# Define relaciones entre usuarios, vendedores y tiendas
# Establece los campos que se almacenan en la base de datos
# Define cómo se representan los datos en el sistema (__str__)

# Este archivo define los modelos del sistema. Extiende el modelo User para crear perfiles 
# de cliente y vendedor, y establece una relación uno a uno entre vendedor y tienda. También define 
# los campos que se almacenan en la base de datos y utiliza relaciones para estructurar correctamente 
# la información. Esto permite organizar los datos de forma clara y mantener integridad en el sistema.


from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ("cc", "Cédula de ciudadanía"),
        ("ce", "Cédula de extranjería"),
        ("ti", "Tarjeta de identidad"),
        ("nit", "NIT"),
        ("pp", "Pasaporte"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    phone = models.CharField(
        max_length=20,
        blank=True
    )
    document_type = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPE_CHOICES,
        blank=True
    )
    document_number = models.CharField(
        max_length=30,
        blank=True
    )
    birth_date = models.DateField(
        null=True,
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

    def __str__(self):
        return f"Perfil de {self.user.username}"


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vendedor: {self.user.username}"


class Store(models.Model):
    seller = models.OneToOneField(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name="store"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
