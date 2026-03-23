# Este archivo define el modelo ContactMessage, que representa los mensajes enviados por los
# usuarios a través del formulario de contacto.

# Define la estructura de la tabla en la base de datos
# Almacena información del usuario y su mensaje
# Clasifica el tipo de solicitud
# Permite gestionar el estado del mensaje (leído/no leído)

# Este archivo define el modelo ContactMessage, que almacena los mensajes enviados por los usuarios. 
# Incluye información personal, contenido del mensaje, tipo de solicitud y preferencia de contacto. 
# También incorpora campos de control como fecha de creación y estado de lectura, y un campo honeypot 
# para prevenir spam. Este modelo es fundamental para gestionar las comunicaciones entrantes desde el
# formulario de contacto.

from django.db import models

class ContactMessage(models.Model):
    SOLICITUD_CHOICES = [
        ("informacion", "Consultas sobre productos"),
        ("queja", "Atencion al cliente"),
        ("reclamo", "Quejas o Reclamos"),
        ("otro", "Otro"),
    ]

    PREFERENCIA_CHOICES = [
        ("correo", "Correo electrónico"),
        ("whatsapp", "Whatsapp"),
    ]

    
    nombre = models.CharField(max_length=120)
    correo = models.EmailField()
    identificacion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    solicitud = models.CharField(max_length=20, choices=SOLICITUD_CHOICES)

    
    asunto = models.CharField(max_length=160)
    mensaje = models.TextField()
    contacto = models.CharField(max_length=20, choices=PREFERENCIA_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    
    honeypot = models.CharField(max_length=200, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.asunto} - {self.correo}"