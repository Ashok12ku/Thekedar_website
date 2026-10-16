import re
from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    """
    Used for both the full Contact/Get-Quote page and the Home page
    quick lead form. Includes custom validation for phone number.
    """

    class Meta:
        model = Inquiry
        fields = [
            "name", "phone", "email", "location",
            "service_selected", "budget_range", "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Your Full Name"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "10-digit Mobile Number"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "Email (optional)"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "City / Area, e.g. Raebareli"
            }),
            "service_selected": forms.Select(attrs={"class": "form-select"}),
            "budget_range": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "Tell us briefly about your project..."
            }),
        }
        labels = {
            "service_selected": "Required Service",
            "budget_range": "Budget Range",
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        # Strip spaces, dashes, and a leading +91 for validation purposes
        digits_only = re.sub(r"[\s\-]", "", phone)
        digits_only = re.sub(r"^\+?91", "", digits_only)

        if not digits_only.isdigit():
            raise forms.ValidationError("Please enter a valid phone number (digits only).")
        if len(digits_only) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        if digits_only[0] not in "6789":
            raise forms.ValidationError("Please enter a valid Indian mobile number.")
        return phone

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Please enter your full name.")
        return name
