from django import forms
from .models import ContactInquiry, ProjectInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "subject", "message"]


class ProjectInquiryForm(forms.ModelForm):
    class Meta:
        model = ProjectInquiry
        fields = ["name", "email", "business_name", "budget_range", "project_type", "message"]
