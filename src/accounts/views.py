from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm
from orders.models import Order
from .forms import UserProfileForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada con éxito. Ahora inicia sesión.")
            return redirect(f"{reverse('login')}?created=1")
        messages.error(request, "Revisa los datos del formulario.")
    else:
        form = SignUpForm()

    return render(request, "pages-general/register_an_account.html", {"form": form})

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

    if request.method == "POST":

        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:

        form = UserProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})