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

        messages.error(request, "Revisa el formulario: hay errores.")
    else:
        form = ContactForm()

    return render(request, "pages-general/contact.html", {"form": form, "sent": False})


def contact_success_view(request):
    form = ContactForm()
    messages.success(request, "Mensaje enviado con éxito.")
    return render(request, "pages-general/contact.html", {"form": form, "sent": True})


def contact_info_view(request):
    return render(request, "pages-general/contact-two.html")