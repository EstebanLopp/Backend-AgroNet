from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

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
    product = get_object_or_404(Product, slug=slug, available=True)

    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:6]

    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "products/product_detail.html", context)