from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'email',
            'nombre',
            'apellido',
            'numero_telefono',
            'tipo_documento',
            'numero_documento',
            'fecha_nacimiento',
            'direccion',
            'departamento',
            'municipio',
        ]

"""
Esto hace lo siguiente:

Usa el sistema de creación de usuario de Django

Maneja confirmación de contraseña automáticamente

Encripta la contraseña correctamente

Usa nuestro modelo personalizado
"""