from django import forms
from .models import JobApplication
from django.forms import ModelForm


class JobApplicationForm(models.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'cv', 'linkedin_url', 'portfolio_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
        }