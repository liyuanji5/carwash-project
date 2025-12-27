from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Booking, Box
from services.models import Service
from customers.models import Customer
from employees.models import Employee
from .forms import UserRegistrationForm, BookingForm


def index(request):
    return render(request, "bookings/index.html")


class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"
    paginate_by = 10

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy("bookings:my_bookings")

    def form_valid(self, form):
        customer = get_object_or_404(Customer, user=self.request.user)
        form.instance.customer = customer
        form.instance.status = "pending"
        return super().form_valid(form)


class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "bookings/my_bookings.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        return Booking.objects.filter(customer=customer).order_by("-booking_date")


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = "bookings/booking_detail.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        customer = get_object_or_404(Customer, user=self.request.user)
        return Booking.objects.filter(customer=customer)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = "bookings/booking_form.html"

    def get_queryset(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        return Booking.objects.filter(customer=customer)

    def get_success_url(self):
        return reverse_lazy("bookings:booking_detail", kwargs={"pk": self.object.pk})


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = "bookings/booking_confirm_delete.html"
    success_url = reverse_lazy("bookings:my_bookings")

    def get_queryset(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        return Booking.objects.filter(customer=customer)


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("bookings:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
