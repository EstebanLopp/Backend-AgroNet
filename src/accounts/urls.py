from django.urls import path
from .views import signup
from . import views

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("cuenta/", views.customer_dashboard, name="customer_dashboard"),
]