from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "address",
            "city",
            "payment_method",
            "shipping_method",
            "notes",
        ]
        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "shipping_method": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if len(address) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")

        return address

    def clean_city(self):
        city = self.cleaned_data["city"].strip()

        if len(city) < 2:
            raise forms.ValidationError("La ciudad debe tener al menos 2 caracteres.")

        return city

    def clean_notes(self):
        notes = self.cleaned_data.get("notes", "").strip()
        return notes