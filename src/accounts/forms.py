from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from datetime import date

from .models import CustomerProfile, Store


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre"
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Apellido"
    )
    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()
        if len(first_name) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()
        if len(last_name) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")

        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if len(username) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.email = self.cleaned_data["email"].strip().lower()

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()
        if len(first_name) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()
        if len(last_name) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ese correo ya está en uso por otro usuario.")

        return email


class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = [
            "phone",
            "document_type",
            "document_number",
            "birth_date",
            "address",
            "city",
        ]
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "document_type": forms.Select(attrs={"class": "form-control"}),
            "document_number": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if phone and not phone.replace(" ", "").replace("+", "").isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números, espacios o el signo +.")

        if phone and len(phone.replace(" ", "").replace("+", "")) < 7:
            raise forms.ValidationError("Ingresa un número de teléfono válido.")

        return phone

    def clean_document_number(self):
        document_number = self.cleaned_data["document_number"].strip()

        if document_number and not document_number.replace(".", "").isdigit():
            raise forms.ValidationError("El número de documento solo debe contener números.")

        if document_number and len(document_number.replace(".", "")) < 5:
            raise forms.ValidationError("Ingresa un número de documento válido.")

        return document_number

    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if address and len(address) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")

        return address

    def clean_city(self):
        city = self.cleaned_data["city"].strip()

        if city and len(city) < 2:
            raise forms.ValidationError("La ciudad debe tener al menos 2 caracteres.")

        return city
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date and birth_date > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return birth_date
    
class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No existe una cuenta registrada con ese correo.")
        return email


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = ["name", "description", "phone", "address"]

        labels = {
            "name": "Nombre de la tienda",
            "description": "Descripción",
            "phone": "Teléfono",
            "address": "Dirección",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "seller-form-e__input"}),
            "description": forms.Textarea(attrs={"class": "seller-form-e__input seller-form-e__textarea", "rows": 3}),
            "phone": forms.TextInput(attrs={"class": "seller-form-e__input"}),
            "address": forms.TextInput(attrs={"class": "seller-form-e__input"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "El nombre de la tienda debe tener al menos 3 caracteres."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not phone.isdigit():
            raise forms.ValidationError(
                "El teléfono solo debe contener números."
            )

        if len(phone) < 7:
            raise forms.ValidationError(
                "El número de teléfono no es válido."
            )

        return phone

    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if len(address) < 5:
            raise forms.ValidationError(
                "La dirección es demasiado corta."
            )

        return address

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        return description