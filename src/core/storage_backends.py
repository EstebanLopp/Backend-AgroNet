import mimetypes
import os
import posixpath
import uuid
from urllib.parse import quote

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from supabase import create_client


@deconstructible
class SupabaseStorage(Storage):
    """
    Storage backend para guardar archivos en Supabase Storage.
    Pensado para archivos públicos, como imágenes de productos.
    """

    def __init__(self, bucket_name=None):
        self.bucket_name = bucket_name or settings.SUPABASE_STORAGE_BUCKET
        self.supabase_url = settings.SUPABASE_URL.rstrip("/")
        self.supabase_key = settings.SUPABASE_KEY
        self.client = create_client(self.supabase_url, self.supabase_key)

    def _clean_name(self, name: str) -> str:
        return str(name).replace("\\", "/").lstrip("/")

    def _public_url(self, name: str) -> str:
        clean_name = quote(self._clean_name(name), safe="/")
        return (
            f"{self.supabase_url}/storage/v1/object/public/"
            f"{self.bucket_name}/{clean_name}"
        )

    def _upload_fileobj(self, fileobj, path: str, upsert: bool) -> str:
        path = self._clean_name(path)

        content_type = getattr(fileobj, "content_type", None)
        if not content_type:
            content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"

        if hasattr(fileobj, "seek"):
            fileobj.seek(0)

        file_data = fileobj.read()

        self.client.storage.from_(self.bucket_name).upload(
            path=path,
            file=file_data,
            file_options={
                "cache-control": "3600",
                "upsert": "true" if upsert else "false",
                "content-type": content_type,
            },
        )
        return path

    def _save(self, name, content):
        """
        Para archivos nuevos, genera un nombre único para evitar colisiones.
        """
        clean_name = self._clean_name(name)
        directory, filename = posixpath.split(clean_name)
        root, ext = os.path.splitext(filename)

        unique_filename = f"{root}-{uuid.uuid4().hex[:12]}{ext.lower()}"
        final_name = (
            posixpath.join(directory, unique_filename)
            if directory
            else unique_filename
        )

        return self._upload_fileobj(content, final_name, upsert=False)

    def upload_existing_file(self, fileobj, path: str):
        """
        Útil para migrar archivos locales existentes conservando el nombre exacto.
        """
        return self._upload_fileobj(fileobj, path, upsert=True)

    def delete(self, name):
        clean_name = self._clean_name(name)
        self.client.storage.from_(self.bucket_name).remove([clean_name])

    def exists(self, name):
        """
        Para archivos nuevos usamos nombres únicos, así que no necesitamos
        preguntar existencia antes de guardar.
        """
        return False

    def url(self, name):
        return self._public_url(name)

    def _open(self, name, mode="rb"):
        clean_name = self._clean_name(name)
        data = self.client.storage.from_(self.bucket_name).download(clean_name)
        return ContentFile(data, name=clean_name)