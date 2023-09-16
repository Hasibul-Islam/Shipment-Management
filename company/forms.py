from django import forms
from .models import CompanyDetails


class CompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        fields = [ 'contact_person', 'customer_company', 'city', 'country', 'state', 'street', 'postal_code', 'email', 'phone', 'best_time_to_call']
        widgets = {
            
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_company': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'best_time_to_call': forms.TextInput(attrs={'class': 'form-control'}),
        }
# 'customer_no': forms.TextInput(attrs={'class': 'form-control'}),