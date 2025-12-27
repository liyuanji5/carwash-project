from django import forms
from .models import Customer


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["phone", "car_model", "car_number", "discount", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
