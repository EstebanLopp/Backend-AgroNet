#Este archivo contiene la lógica del catálogo de productos y del panel de gestión para vendedores. Aquí se manejan tanto las vistas públicas del catálogo como las operaciones privadas de creación, edición y administración de productos. Este archivo es clave porque conecta directamente: catálogo público, detalle de productos, gestión de productos del vendedor, tienda del vendedor,carrito y pedidos

#Lista productos publicados y visibles, Filtra por categoría y búsqueda, Muestra detalle de un producto, Permite al vendedor ver sus productos, Permite crear productos, Permite editar productos, Permite activar o desactivar productos, Permite ver el detalle interno de un producto del vendedor

#Este archivo contiene la lógica del catálogo y del panel de productos para vendedores. Permite listar y buscar productos públicos con filtros y paginación, mostrar su detalle y gestionar productos dentro de la tienda del vendedor. Además, aplica validaciones de acceso y reglas de visibilidad para asegurar que solo se muestren productos válidos y que cada vendedor administre únicamente sus propios productos.

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q #->permite busquedas combinadas
from django.core.paginator import Paginator #->divide resultados en paginas
from django.contrib.auth.decorators import login_required #->pretege vistas privadas
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm
from accounts.models import SellerProfile

#Muestra el catálogo público de productos visibles.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    #Solo muestra productos que: están disponibles, están publicados, pertenecen a tiendas activas
    products = Product.objects.filter(
        available=True,
        status="published",
        store__is_active=True
    )
    
    #obtiene texto de búsqueda enviado por URL
    query = request.GET.get("q")

    #obtiene la categoría por slug, filtra productos de esa categoría
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    #busqueda por nombre o descripción
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    #divide productos en páginas de 6 y mejora rendimiento y experiencia de usuario
    paginator = Paginator(products, 6)  # 6 productos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "categories": categories,
        "page_obj": page_obj,
        "query": query,
        
    }

    return render(request, "products/catalog.html", context)

#Muestra el detalle de un producto específico.
#solo se pueden ver productos válidos públicamente
def product_detail(request, slug):
    product = get_object_or_404(
    Product,
    slug=slug,
    available=True,
    status="published",
    store__is_active=True
)

    #muestra productos de la misma categoría, excluye el actual y limita a 6
    related_products = Product.objects.filter(
        category=product.category,
        available=True,
        status="published",
        store__is_active=True
    ).exclude(id=product.id)[:6]

    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "products/product_detail.html", context)

#------------------------------------------------------------------

#Busca la tienda asociada al usuario vendedor. 
def get_seller_store(user):
    #centraliza una validación repetida, evita duplicar lógica en varias vistas
    seller_profile = SellerProfile.objects.filter(user=user).first()

    if not seller_profile:
        return None

    return getattr(seller_profile, "store", None)

#Muestra todos los productos de la tienda del vendedor autenticado.
@login_required
def my_products(request):
    store = get_seller_store(request.user)

    #solo vendedores con tienda pueden gestionar productos
    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    #filtrar por estado
    status = request.GET.get("status", "all")
    #trae categoría relacionada de forma optimizada
    products = Product.objects.filter(store=store).select_related("category")
    #permite ver todos, publicados o deshabilitados
    if status == "published":
        products = products.filter(status="published")
    elif status == "disabled":
        products = products.filter(status="disabled")

    context = {
        "store": store,
        "products": products,
        "current_status": status,
    }

    return render(request, "products/my_products.html", context)

#Permite al vendedor registrar un nuevo producto.
@login_required
def create_product(request):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        #asocia el producto a la tienda del vendedor y completa el campo productor automáticamente
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.producer = store.name
            product.save()

            messages.success(request, "Producto registrado correctamente.")
            return redirect("products:my_products")
        else:
            print(form.errors)
            messages.error(request, "Revisa los campos del formulario.")
    else:
        form = ProductForm()

    context = {
        "form": form,
    }

    return render(request, "products/create_product.html", context)

#Permite modificar un producto existente del vendedor.
@login_required
def update_product(request, pk):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    #garantiza que el vendedor solo puede editar productos de su propia tienda
    product = get_object_or_404(Product, pk=pk, store=store)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

            #mantiene consistencia entre estado y disponibilidad
            if product.status == "published":
                product.available = True
            else:
                product.available = False

            product.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("products:my_products")
        else:
            messages.error(request, "No se pudo actualizar el producto.")
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "product": product,
    }

    return render(request, "products/update_product.html", context)

#Cambia el estado del producto entre publicado y deshabilitado.
@login_required
def toggle_product_status(request, pk):
    store = get_seller_store(request.user)

    product = get_object_or_404(Product, pk=pk, store=store)

    #si está deshabilitado, lo publica, si está publicado, lo deshabilita
    if product.status == "disabled":
        product.status = "published"
        product.available = True
    else:
        product.status = "disabled"
        product.available = False

    product.save()

    return redirect("products:my_products")


#Muestra el detalle interno de un producto de la tienda del vendedor.
@login_required
def seller_product_detail(request, pk):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")
    #solo el dueño de la tienda puede ver ese detalle interno
    product = get_object_or_404(Product, pk=pk, store=store)

    context = {
        "product": product,
    }

    return render(request, "products/seller_product_detail.html", context)