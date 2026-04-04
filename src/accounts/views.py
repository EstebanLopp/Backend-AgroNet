# Este archivo contiene la lógica principal del sistema para la gestión de usuarios, perfiles y tiendas.
# Aquí se conectan los formularios, modelos y templates.

# Maneja el registro de usuarios
# Controla el dashboard del cliente
# Permite editar perfil
# Gestiona eliminación de cuenta
# Administra la creación y gestión de tiendas
# Controla el panel del vendedor
# Muestra tiendas públicamente

# Este archivo contiene la lógica principal del sistema. Maneja el registro de usuarios, 
# edición de perfil, gestión de cuentas y administración de tiendas. Implementa buenas prácticas 
# como validación de formularios, protección de rutas, eliminación lógica de usuarios y optimización 
# de consultas. Es el punto donde se conectan los modelos, formularios y templates para responder a las 
# solicitudes del usuario.

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from orders.models import Order, SellerNotification
from .models import CustomerProfile, SellerProfile
from django.contrib import messages
from django.utils import timezone

from .forms import SignUpForm, UserProfileForm, CustomerProfileForm, StoreForm

from django.shortcuts import render, get_object_or_404
from accounts.models import Store
from products.models import Product


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Tu cuenta fue creada correctamente. Completa tu perfil para continuar.")
            return redirect("accounts:dashboard")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def customer_dashboard(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by("-created")

    total_orders = orders.count()
    total_spent = sum(order.get_total_price() for order in orders)
    last_order = orders.first()
    last_orders = orders[:3]

    seller_profile = SellerProfile.objects.filter(user=request.user).first()
    has_store = False

    if seller_profile and hasattr(seller_profile, "store"):
        has_store = True

    context = {
        "profile": profile,
        "total_orders": total_orders,
        "total_spent": total_spent,
        "last_order": last_order,
        "last_orders": last_orders,
        "has_store": has_store,
    }

    return render(request, "accounts/dashboard.html", context)


@login_required
def edit_profile(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Tu perfil fue actualizado correctamente.")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "No se pudo actualizar el perfil. Revisa los campos marcados.")
            
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = CustomerProfileForm(instance=profile)
        

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/profile.html", context)

@login_required
def delete_account(request):
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect("accounts:dashboard")

    user = request.user

    if user.is_staff or user.is_superuser:
        messages.error(request, "No puedes eliminar esta cuenta desde esta opción.")
        return redirect("accounts:dashboard")

    if not CustomerProfile.objects.filter(user=user).exists():
        messages.error(request, "Solo los clientes pueden usar esta opción.")
        return redirect("accounts:dashboard")

    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    original_id = user.id

    user.username = f"deleted_user_{original_id}_{timestamp}"

    if user.email:
        user.email = f"deleted_{original_id}_{timestamp}@deleted.local"

    user.first_name = ""
    user.last_name = ""
    user.is_active = False
    user.save()

    CustomerProfile.objects.filter(user=user).update(
        phone="",
        document_type="",
        document_number="",
        birth_date=None,
        address="",
        city="",
    )

    logout(request)
    messages.success(request, "Tu cuenta fue eliminada correctamente.")
    return redirect("index")


@login_required
def create_store(request):
    seller_profile, _ = SellerProfile.objects.get_or_create(user=request.user)
    customer_profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if hasattr(seller_profile, "store"):
        messages.info(request, "Ya tienes una tienda registrada.")
        return redirect("accounts:dashboard")

    if not customer_profile.document_type or not customer_profile.document_number:
        messages.error(
            request,
            "Debes completar tu tipo y número de documento en tu perfil antes de crear una tienda."
        )
        return redirect("accounts:edit_profile")
        
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.seller = seller_profile
            store.save()
            messages.success(request, "Tu tienda fue creada correctamente.")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "No se pudo crear la tienda. Revisa los campos del formulario.")
    else:
        form = StoreForm()

    return render(request, "accounts/create_store.html", {"form": form})


@login_required
def seller_dashboard(request):
    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile or not hasattr(seller_profile, "store"):
        messages.error(request, "Primero debes crear una tienda.")
        return redirect("accounts:create_store")

    store = seller_profile.store

    unread_notifications_count = store.notifications.filter(is_read=False).count()
    recent_notifications = (
        store.notifications
        .select_related("order", "order__user")
        .order_by("-created_at")[:5]
    )

    context = {
        "store": store,
        "unread_notifications_count": unread_notifications_count,
        "recent_notifications": recent_notifications,
    }

    return render(request, "accounts/seller_dashboard.html", context)

def public_store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)

    products = Product.objects.filter(
        store=store,
        status="published",
        available=True,
        stock__gt=0
    ).select_related("category")

    context = {
        "store": store,
        "products": products,
    }
    return render(request, "accounts/public_store_detail.html", context)


@login_required
def edit_store(request):
    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile or not hasattr(seller_profile, "store"):
        messages.error(request, "Primero debes crear una tienda.")
        return redirect("accounts:create_store")

    store = seller_profile.store

    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)

        if form.is_valid():
            form.save()
            messages.success(request, "Los datos de tu tienda fueron actualizados correctamente.")
            return redirect("accounts:seller_dashboard")
        else:
            messages.error(request, "No se pudo actualizar la tienda. Revisa los campos del formulario.")
    else:
        form = StoreForm(instance=store)

    context = {
        "form": form,
        "store": store,
    }

    return render(request, "accounts/edit_store.html", context)


@login_required
def toggle_store_status(request):
    
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect("accounts:seller_dashboard")

    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if not seller_profile:
        messages.error(request, "No tienes perfil de vendedor.")
        return redirect("accounts:seller_dashboard")

    store = getattr(seller_profile, "store", None)

    if not store:
        messages.error(request, "No tienes una tienda registrada.")
        return redirect("accounts:create_store")

    store.is_active = not store.is_active
    store.save()

    if store.is_active:
        messages.success(request, "Tu tienda ha sido habilitada.")
    else:
        messages.success(request, "Tu tienda ha sido deshabilitada.")

    return redirect("accounts:seller_dashboard")

