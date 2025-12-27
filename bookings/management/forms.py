from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, label="Телефон")
    car_model = forms.CharField(
        max_length=100, required=False, label="Марка автомобиля"
    )
    car_number = forms.CharField(max_length=20, required=False, label="Госномер")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Создаем профиль клиента
            from customers.models import Customer

            Customer.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                car_model=self.cleaned_data["car_model"],
                car_number=self.cleaned_data["car_number"],
            )
        return user


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["service", "booking_date", "booking_time"]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "booking_time": forms.TimeInput(attrs={"type": "time"}),
        }
