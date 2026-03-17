from django.urls import path
from .views import signup
from . import views
from .views import customer_dashboard
from .forms import CustomPasswordResetForm
from .views import edit_profile
from django.contrib.auth import views as auth_views
from .views import public_store_detail

app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("cuenta/", customer_dashboard, name="dashboard"),
    path("perfil/", edit_profile, name="edit_profile"),
    path("crear-tienda/", views.create_store, name="create_store"),
    path("tienda/<int:pk>/", public_store_detail, name="public_store_detail"),
    path("mi-tienda/", views.seller_dashboard, name="seller_dashboard"),
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
    ),
    name="password_reset",
),
path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html",
    ),
    name="password_reset_done",
),
path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
    ),
    name="password_reset_confirm",
),
path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html",
    ),
    name="password_reset_complete",
),
]