from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.index, name="index"),
    path("bookings/", views.BookingCreateView.as_view(), name="create_booking"),
    path("bookings/my/", views.MyBookingsView.as_view(), name="my_bookings"),
    path(
        "bookings/<int:pk>/", views.BookingDetailView.as_view(), name="booking_detail"
    ),
    path(
        "bookings/<int:pk>/edit/",
        views.BookingUpdateView.as_view(),
        name="edit_booking",
    ),
    path(
        "bookings/<int:pk>/delete/",
        views.BookingDeleteView.as_view(),
        name="delete_booking",
    ),
]
