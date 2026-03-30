# Este archivo define el formulario de checkout, es decir, el formulario que el usuario completa al momento de realizar un pedido. (Este archivo es clave porque está en el flujo de compra.)

# Crea un formulario basado en el modelo Order, Captura información de envío y pago, Valida los datos antes de crear el pedido, Aplica estilos para integración con el frontend

# Este archivo define el formulario de checkout del sistema. Permite capturar y validar la información necesaria para crear un pedido, como dirección, ciudad, método de pago y envío. Está basado en el modelo Order y garantiza que los datos ingresados sean válidos antes de procesar la compra.

from django import forms
from .models import Order
import re

#Está conectado directamente al modelo Order, permite crear pedidos desde el formulario
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        #campos
        fields = [
            "address",
            "city",
            "payment_method",
            "shipping_method",
            "notes",
        ]

        #Aplica clases CSS, Integra el formulario con el diseño del frontend
        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "shipping_method": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    # Validacion de la dirección
    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if len(address) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")

        if not any(char.isalpha() for char in address):
            raise forms.ValidationError("La dirección debe incluir texto válido.")

        return address

    # Validacion de la ciudad
    def clean_city(self):
        city = self.cleaned_data["city"].strip()

        if len(city) < 2:
            raise forms.ValidationError("La ciudad debe tener al menos 2 caracteres.")

        if re.search(r'\d', city):
            raise forms.ValidationError("La ciudad no puede contener números.")

        return city.title()

    # Limpieza de notas (Elimina espacios innecesarios, No aplica validación estricta)
    def clean_notes(self):
        notes = self.cleaned_data.get("notes", "").strip()

        if len(notes) > 300:
            raise forms.ValidationError("Las notas no pueden superar los 300 caracteres.")

        return notes


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "seller-notification-detail__status-select"}),
        }