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

    # Datos personales (18_personal_details.html)
    nombre = models.CharField(max_length=120)
    correo = models.EmailField()
    identificacion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    solicitud = models.CharField(max_length=20, choices=SOLICITUD_CHOICES)

    # Mensaje (19_message.html)
    asunto = models.CharField(max_length=160)
    mensaje = models.TextField()
    contacto = models.CharField(max_length=20, choices=PREFERENCIA_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # Anti-spam simple
    honeypot = models.CharField(max_length=200, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.asunto} - {self.correo}"