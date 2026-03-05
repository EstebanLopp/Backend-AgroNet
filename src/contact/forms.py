from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = [
            "nombre", "correo", "identificacion", "telefono", "solicitud",
            "asunto", "mensaje", "contacto",
            "honeypot",
        ]

    def clean_honeypot(self):
        value = (self.cleaned_data.get("honeypot") or "").strip()
        if value:
            raise forms.ValidationError("Spam detectado.")
        return value