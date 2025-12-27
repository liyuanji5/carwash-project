from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Customer
from .forms import CustomerUpdateForm


class CustomerProfileView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "customers/profile.html"
    context_object_name = "customer_profile"

    def get_object(self):
        return get_object_or_404(Customer, user=self.request.user)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    template_name = "customers/profile_edit.html"

    def get_object(self):
        return get_object_or_404(Customer, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("customers:profile", kwargs={"pk": self.object.pk})
