from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm
from accounts.models import SellerProfile


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(
        available=True,
        status="published",
        store__is_active=True
    )
    

    query = request.GET.get("q")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Paginación
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

def product_detail(request, slug):
    product = get_object_or_404(
    Product,
    slug=slug,
    available=True,
    status="published",
    store__is_active=True
)

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
    
def get_seller_store(user):
    seller_profile = SellerProfile.objects.filter(user=user).first()

    if not seller_profile:
        return None

    return getattr(seller_profile, "store", None)


@login_required
def my_products(request):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    status = request.GET.get("status", "all")

    products = Product.objects.filter(store=store).select_related("category")

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


@login_required
def create_product(request):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

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


@login_required
def update_product(request, pk):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    product = get_object_or_404(Product, pk=pk, store=store)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

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


@login_required
def toggle_product_status(request, pk):
    store = get_seller_store(request.user)

    product = get_object_or_404(Product, pk=pk, store=store)

    if product.status == "disabled":
        product.status = "published"
        product.available = True
    else:
        product.status = "disabled"
        product.available = False

    product.save()

    return redirect("products:my_products")


@login_required
def seller_product_detail(request, pk):
    store = get_seller_store(request.user)

    if not store:
        messages.error(request, "Primero debes registrar tu tienda.")
        return redirect("accounts:create_store")

    product = get_object_or_404(Product, pk=pk, store=store)

    context = {
        "product": product,
    }

    return render(request, "products/seller_product_detail.html", context)