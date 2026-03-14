from django.urls import path
from .views import (
    product_list,
    product_detail,
    my_products,
    create_product,
    update_product,
    toggle_product_status,
    seller_product_detail,
)

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("p/<slug:slug>/", product_detail, name="product_detail"),

    # panel vendedor
    path("mis-productos/", my_products, name="my_products"),
    path("mis-productos/crear/", create_product, name="create_product"),
    path("mis-productos/<int:pk>/", seller_product_detail, name="seller_product_detail"),
    path("mis-productos/<int:pk>/editar/", update_product, name="update_product"),
    path("mis-productos/<int:pk>/estado/", toggle_product_status, name="toggle_product_status"),

    #categorias
    path("categoria/<slug:category_slug>/", product_list, name="products_by_category"),
]


