# Este archivo define la configuración básica de la aplicación core dentro del proyecto Django.

# Registra la aplicación core en el sistema
# Define su nombre interno
# Sirve como punto de extensión para futuras configuraciones globales

# Este archivo define la configuración básica de la aplicación core. Este módulo se utiliza para centralizar
# funcionalidades reutilizables del sistema, como servicios, y su configuración permite integrarlo 
# correctamente dentro del proyecto Django. Es una estructura estándar que facilita la gestión y extensión 
# de la aplicación en el futuro.

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
