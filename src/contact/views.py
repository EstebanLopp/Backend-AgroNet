# Este archivo contiene la lógica del sistema de contacto.
# Se encarga de procesar el formulario, guardar los mensajes y gestionar el envío de correos de confirmación.

# Muestra el formulario de contacto
# Valida y guarda mensajes
# Envía correo de confirmación al usuario
# Maneja vistas de éxito e información adicional

# Este archivo maneja la lógica del formulario de contacto. Permite recibir, validar y almacenar 
# mensajes de los usuarios, además de enviar un correo de confirmación utilizando plantillas HTML. 
# Está diseñado siguiendo buenas prácticas como separación de responsabilidades, manejo de errores y
# control de métodos HTTP, lo que garantiza una experiencia de usuario fluida y segura.

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from core.services.email_service import send_templated_email
from .forms import ContactForm

@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = form.save()  

            
            try:
                send_templated_email(
                    subject="AgroNet: recibimos tu mensaje",
                    to=[obj.correo],
                    template_html="emails/contact_received.html",
                    context={
                        "nombre": obj.nombre,
                        "asunto": obj.asunto,
                        "mensaje": obj.mensaje,
                        "solicitud_label": obj.get_solicitud_display(),
                    },
                )
            except Exception:
                
                pass

            return redirect("contact:contact_success")

    else:
        form = ContactForm()

    return render(request, "pages-general/contact.html", {"form": form, "sent": False})


def contact_success_view(request):
    form = ContactForm()
    messages.success(request, "Mensaje enviado con éxito.")
    return render(request, "pages-general/contact.html", {"form": form, "sent": True})


def contact_info_view(request):
    return render(request, "pages-general/contact-two.html")