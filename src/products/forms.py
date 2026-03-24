#Este archivo define el formulario para la creación y edición de productos en el sistema. Permite que los vendedores registren productos con validaciones adecuadas.

#Crea un formulario basado en el modelo Product, Valida los datos antes de guardar productos, Controla reglas de negocio (precio, stock, peso, etc.),Define etiquetas para mejorar la interfaz


#Este archivo define el formulario para crear y editar productos. Utiliza un ModelForm para validar y guardar la información, asegurando que los datos cumplan reglas como precio positivo, stock válido y obligatoriedad de imagen. Esto garantiza que los productos registrados sean consistentes y aptos para el sistema de ventas.


from django import forms
from .models import Product

#Está conectado directamente al modelo Product y permite crear o editar productos desde formularios
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "unit",
            "image",
            "stock",
            "status",
            "shipping_type",
            "weight_unit",
            "weight",
            "delivery_time",
            "payment_type",
        ]
        labels = {
            "category": "Categoría",
            "name": "Nombre del producto",
            "description": "Descripción",
            "price": "Precio",
            "unit": "Unidad de venta",
            "image": "Imagen del producto",
            "stock": "Cantidad disponible",
            "status": "Estado",
            "shipping_type": "Tipo de envío",
            "weight_unit": "Unidad de peso",
            "weight": "Peso",
            "delivery_time": "Entrega estimada",
            "payment_type": "Tipo de pago",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError(
                "El nombre del producto debe tener al menos 3 caracteres."
            )
        return name

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError(
                "El precio debe ser mayor que cero."
            )
        return price

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        if stock < 0:
            raise forms.ValidationError(
                "La cantidad disponible no puede ser negativa."
            )
        return stock

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if len(description) < 10:
            raise forms.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )
        return description

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is not None and weight <= 0:
            raise forms.ValidationError(
                "El peso debe ser mayor que cero."
            )
        return weight

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            raise forms.ValidationError("Debes subir una imagen del producto.")

        return image