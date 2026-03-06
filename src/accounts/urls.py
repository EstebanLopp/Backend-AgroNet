from django.urls import path
from .views import signup
from . import views
from .views import customer_dashboard
from .views import edit_profile

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("cuenta/", views.customer_dashboard, name="customer_dashboard"),
    path("cuenta/", customer_dashboard, name="dashboard"),
    path("perfil/", edit_profile, name="edit_profile"),
]