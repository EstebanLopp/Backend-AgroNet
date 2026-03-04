from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

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