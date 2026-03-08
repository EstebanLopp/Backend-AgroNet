from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib import messages

from .forms import SignUpForm, UserProfileForm, CustomerProfileForm


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

    context = {
        "total_orders": total_orders,
        "total_spent": total_spent,
        "last_order": last_order,
        "last_orders": last_orders,
    }

    return render(request, "accounts/dashboard.html", context)


@login_required
def edit_profile(request):
    profile, _ = request.user.customer_profile, True

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