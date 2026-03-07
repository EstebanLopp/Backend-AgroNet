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