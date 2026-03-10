from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "document_type", "document_number", "city")
    search_fields = ("user__username", "user__email", "document_number", "phone", "city")