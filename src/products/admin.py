#Este archivo configura el panel de administración para gestionar categorías y productos del sistema.

#Registra los modelos Category y Product en el admin, Permite administrar el catálogo de productos, Facilita la búsqueda, filtrado y visualización de productos y genera automáticamente el slug a partir del nombre

#Este archivo configura el panel de administración para gestionar categorías y productos. Permite visualizar información clave, filtrar y buscar productos, y utiliza slugs para generar URLs amigables automáticamente, facilitando la administración del catálogo del sistema.

#evita que el admin lo escriba manualmente
from django.contrib import admin
from .models import Category, Product

#registro del modelo
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #columnas visibles
    list_display = ('name', 'slug')
    #genera automáticamente el slug a partir del nombre, evita que el admin lo escriba manualmente
    prepopulated_fields = {'slug': ('name',)}


#Registro del modelo
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #Columnas visibles
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at')
    #filtrar productos activos/inactivos, filtrar por categoría
    list_filter = ('available', 'category')
    #busqueda
    search_fields = ('name', 'description')
    #slug automatico
    prepopulated_fields = {'slug': ('name',)}