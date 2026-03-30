# Este archivo define todos los formularios del sistema relacionados con:

# Registro de usuarios
# Edición de perfil
# Perfil de cliente
# Recuperación de contraseña
# Creación/edición de tienda

# Centraliza la validación de datos antes de guardarlos en la base de datos.

# Extiende formularios de Django (UserCreationForm, ModelForm, PasswordResetForm)
# Valida datos ingresados por el usuario
# Normaliza información (ej: emails en minúsculas, eliminación de espacios)
# Controla reglas de negocio (edad mínima, unicidad de email, etc.)


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from datetime import date
import re


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

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True

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

        if len(city) < 2:
            raise forms.ValidationError("La ciudad debe tener al menos 2 caracteres.")

        if re.search(r'\d', city):
            raise forms.ValidationError("La ciudad no puede contener números.")

        return city.title()

    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")

        if not birth_date:
            return birth_date

        today = date.today()

        if birth_date > today:
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")

        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        if age < 18:
            raise forms.ValidationError("Debes ser mayor de edad para registrarte.")

        return birth_date
    
class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("No existe una cuenta registrada con ese correo.")

        return email


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = ["name", "description", "phone", "address", "city"]

        labels = {
            "name": "Nombre de la tienda",
            "description": "Descripción",
            "phone": "Teléfono",
            "address": "Dirección",
            "city": "Ciudad"
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "seller-form-e__input"}),
            "description": forms.Textarea(attrs={"class": "seller-form-e__input seller-form-e__textarea", "rows": 3}),
            "phone": forms.TextInput(attrs={"class": "seller-form-e__input"}),
            "address": forms.TextInput(attrs={"class": "seller-form-e__input"}),
            "city": forms.TextInput(attrs={"class": "seller-form-e__input"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise forms.ValidationError("El nombre de la tienda es obligatorio.")

        if len(name) < 3:
            raise forms.ValidationError(
                "El nombre de la tienda debe tener al menos 3 caracteres."
            )

        return name.title()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            raise forms.ValidationError("El teléfono es obligatorio.")

        if not re.match(r'^[0-9+\-\s]+$', phone):
            raise forms.ValidationError(
                "El teléfono solo puede contener números, espacios, + o -."
            )

        phone_digits = re.sub(r'\D', '', phone)

        if len(phone_digits) < 7:
            raise forms.ValidationError(
                "El número de teléfono no es válido."
            )

        return phone

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()

        if not address:
            raise forms.ValidationError("La dirección es obligatoria.")

        if len(address) < 5:
            raise forms.ValidationError(
                "La dirección es demasiado corta."
            )

        return address

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()

        if not description:
            raise forms.ValidationError("La descripción es obligatoria.")

        if len(description) < 10:
            raise forms.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )

        return description

    def clean_city(self):
        city = self.cleaned_data.get("city", "").strip()

        if not city:
            raise forms.ValidationError("La ciudad es obligatoria.")

        if len(city) < 3:
            raise forms.ValidationError(
                "La ciudad debe tener al menos 3 caracteres."
            )

        if re.search(r'\d', city):
            raise forms.ValidationError(
                "La ciudad no puede contener números."
            )

        return city.title()