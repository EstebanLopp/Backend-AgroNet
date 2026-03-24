# Este archivo define la configuración de la aplicación Inicio, que generalmente corresponde a la página principal del sistema.

# Sirve para Registrar la aplicación Inicio dentro del proyecto Django, define su nombre interno y permite agregar configuraciones adicionales si se requieren en el futuro

#Este archivo define la configuración básica de la aplicación inicio, que corresponde a la página principal del sistema. Permite registrar la app dentro del proyecto y mantener una estructura modular organizada.

from django.apps import AppConfig

#Hereda de AppConfig y representa la configuración de la aplicación dentro del proyecto
class InicioConfig(AppConfig):
    #Define el nombre con el que Django identifica la app y debe coincidir con el nombre del directorio
    name = 'Inicio'
