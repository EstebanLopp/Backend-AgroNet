from django.contrib import admin
from .models import Order, OrderItem, SellerNotification


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created",
        "paid",
        "status",
        "payment_method",
        "shipping_method",
        "city",
    )
    list_filter = ("paid", "status", "payment_method", "shipping_method", "created")
    search_fields = ("id", "user__username", "user__email", "address", "city")
    inlines = [OrderItemInline]

@admin.register(SellerNotification)
class SellerNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "order", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "store")
    search_fields = ("store__name", "order__id", "order__user__username")