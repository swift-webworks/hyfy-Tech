import time

from django import forms
from django.core.exceptions import ValidationError

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    # Honeypot field: real visitors never see or fill this (hidden via CSS).
    # Any bot that fills it out gets silently rejected.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    # Timestamp of when the form was rendered, used to reject submissions
    # that happen implausibly fast (a strong signal of automated spam).
    form_rendered_at = forms.FloatField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Enquiry
        fields = [
            "coordinator_name",
            "email",
            "phone_number",
            "required_date",
            "facility_type",
            "service_required",
            "brand",
            "location",
            "message",
        ]
        widgets = {
            "coordinator_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Coordinator Name", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address", "required": True}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number", "required": True}),
            "required_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "facility_type": forms.TextInput(attrs={"class": "form-control", "placeholder": "Place / Facility Type"}),
            "service_required": forms.Select(attrs={"class": "form-select", "required": True}),
            "brand": forms.TextInput(attrs={"class": "form-control", "placeholder": "Brand (if known)"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Location"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Tell us about your requirement"}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise ValidationError("Spam detected.")
        return value

    def clean_form_rendered_at(self):
        rendered_at = self.cleaned_data.get("form_rendered_at")
        if rendered_at:
            elapsed = time.time() - rendered_at
            if elapsed < 3:
                raise ValidationError("Please take a moment to review the form before submitting.")
        return rendered_at

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number", "").strip()
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise ValidationError("Please enter a valid phone number.")
        return phone
