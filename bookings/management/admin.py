from django.contrib import admin
from .models import Booking, Box


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "service",
        "booking_date",
        "booking_time",
        "status",
        "total_price",
    )
    list_filter = ("status", "booking_date", "box")
    search_fields = (
        "customer__user__username",
        "customer__user__email",
        "customer__phone",
    )
    date_hierarchy = "booking_date"
    ordering = ("-booking_date", "-booking_time")


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ("number", "box_type", "capacity", "is_active")
    list_filter = ("box_type", "is_active")
