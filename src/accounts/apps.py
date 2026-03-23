# Este archivo define la configuración de la aplicación accounts dentro del proyecto Django.
# Permite inicializar comportamientos específicos cuando la aplicación se carga.

# Registra la aplicación accounts en Django.
# Define el tipo de campo automático por defecto.
# Ejecuta código adicional al iniciar la app (carga de señales).

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals