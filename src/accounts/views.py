from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import CustomerProfile, SellerProfile
from django.contrib import messages

from .forms import SignUpForm, UserProfileForm, CustomerProfileForm, StoreForm


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
def create_store(request):
    seller_profile, _ = SellerProfile.objects.get_or_create(user=request.user)

    if hasattr(seller_profile, "store"):
        messages.info(request, "Ya tienes una tienda registrada.")
        return redirect("accounts:dashboard")

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

    context = {
        "store": store
    }

    return render(request, "accounts/seller_dashboard.html", context)