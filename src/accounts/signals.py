# Este archivo define señales en Django que permiten ejecutar lógica automáticamente cuando ocurren 
# eventos en los modelos, en este caso cuando se crea o guarda un usuario.

# Escucha eventos del modelo User
# Crea automáticamente un CustomerProfile cuando se registra un usuario
# Mantiene sincronizado el perfil del cliente cuando el usuario se guarda

# Este archivo define señales que permiten ejecutar lógica automáticamente cuando se guarda 
# un usuario. En este caso, se crea un perfil de cliente de forma automática al registrarse un 
# usuario, y se mantiene sincronizado cada vez que el usuario se actualiza. Esto asegura consistencia 
# en los datos sin necesidad de intervención manual

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    if hasattr(instance, "customer_profile"):
        instance.customer_profile.save()