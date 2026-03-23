# Este archivo implementa un servicio reutilizable para el envío de correos electrónicos usando
# plantillas dinámicas. Centraliza la lógica de envío de emails en el sistema.

# Genera correos a partir de templates HTML y opcionalmente texto plano
# Inserta datos dinámicos en las plantillas
# Envía correos usando el sistema de Django
# Permite reutilizar esta funcionalidad en diferentes módulos

# Este archivo define un servicio para enviar correos electrónicos usando plantillas dinámicas. 
# Permite separar la lógica de envío del resto del sistema, facilitando la reutilización y el mantenimiento.
# Utiliza EmailMultiAlternatives para enviar correos en formato HTML y texto, y obtiene la configuración 
# desde settings para mayor flexibilidad.

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_templated_email(
    *,
    subject: str,
    to: list[str],
    template_html: str,
    context: dict,
    template_txt: str | None = None,
    reply_to: list[str] | None = None,
) -> None:
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    html_body = render_to_string(template_html, context)
    text_body = render_to_string(template_txt, context) if template_txt else ""

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to,
        reply_to=reply_to or None,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)