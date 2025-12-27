from django import forms
from .models import Employee, Position


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["position", "phone", "hire_date", "is_active"]
        widgets = {
            "hire_date": forms.DateInput(attrs={"type": "date"}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
