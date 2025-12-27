from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("profile/", views.CustomerProfileView.as_view(), name="profile"),
    path("profile/edit/", views.CustomerUpdateView.as_view(), name="edit_profile"),
]
