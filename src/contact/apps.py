# Este archivo define la configuración básica de la aplicación contact dentro del proyecto Django.

# Registra la aplicación en el sistema de Django
# Define su nombre interno
# Permite agregar configuraciones adicionales si se necesitan en el futuro

# Este archivo define la configuración básica de la aplicación contact en Django.
# Es una estructura estándar que permite registrar la app dentro del proyecto y sirve como punto 
# de extensión para agregar configuraciones adicionales si fueran necesarias

from django.apps import AppConfig


class ContactConfig(AppConfig):
    name = 'contact'
