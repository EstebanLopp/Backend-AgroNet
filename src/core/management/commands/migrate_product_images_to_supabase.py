from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Sube a Supabase las imágenes locales de productos conservando la ruta guardada en la BD."

    def handle(self, *args, **options):
        image_field = Product._meta.get_field("image")
        storage = image_field.storage

        uploaded = 0
        missing = 0

        products = Product.objects.exclude(image="").exclude(image__isnull=True)

        for product in products:
            image_name = str(product.image.name).replace("\\", "/")
            local_path = Path(settings.BASE_DIR) / "media" / image_name

            if not local_path.exists():
                self.stdout.write(
                    self.style.WARNING(f"No existe localmente: {image_name}")
                )
                missing += 1
                continue

            with local_path.open("rb") as f:
                storage.upload_existing_file(f, image_name)

            self.stdout.write(self.style.SUCCESS(f"Subida: {image_name}"))
            uploaded += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Imágenes subidas: {uploaded}"))
        self.stdout.write(self.style.WARNING(f"Imágenes no encontradas localmente: {missing}"))