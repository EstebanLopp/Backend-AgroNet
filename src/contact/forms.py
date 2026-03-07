from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = [
            "nombre",
            "identificacion",
            "correo",
            "telefono",
            "asunto",
            "mensaje",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "identificacion": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "mensaje": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }

    def clean_honeypot(self):
        honeypot = self.cleaned_data.get("honeypot")
        if honeypot:
            raise forms.ValidationError("Spam detectado.")
        return honeypot

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")

        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no debe contener números.")

        return nombre

    def clean_identificacion(self):
        identificacion = self.cleaned_data["identificacion"].strip()

        if not identificacion.replace(".", "").isdigit():
            raise forms.ValidationError("La identificación solo debe contener números.")

        if len(identificacion.replace(".", "")) < 5:
            raise forms.ValidationError("Ingresa una identificación válida.")

        return identificacion

    def clean_correo(self):
        return self.cleaned_data["correo"].strip().lower()

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()

        clean_phone = telefono.replace(" ", "").replace("+", "").replace("-", "")

        if not clean_phone.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números, espacios, guiones o el signo +.")

        if len(clean_phone) < 7:
            raise forms.ValidationError("Ingresa un número de teléfono válido.")

        return telefono

    def clean_asunto(self):
        asunto = self.cleaned_data["asunto"].strip()

        if len(asunto) < 4:
            raise forms.ValidationError("El asunto debe tener al menos 4 caracteres.")

        return asunto

    def clean_mensaje(self):
        mensaje = self.cleaned_data["mensaje"].strip()

        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")

        return mensaje