from django import forms
from .models import CNFInfo

class ShipmentForm(forms.ModelForm):
    class Meta:
        PAYMENT_STATUS_CHOICES = (
        (False, 'Pending'),
        (True, 'Paid')
        )

        payment_status = forms.ChoiceField(choices=PAYMENT_STATUS_CHOICES, widget=forms.RadioSelect)
        model = CNFInfo
        fields = ['cnf_information','contact_person', 'city', 'country', 'state', 'street', 'postal_code', 'email', 'phone', 'best_time_to_call']
        widgets = {
            
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'cnf_information': forms.Textarea(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'best_time_to_call': forms.TextInput(attrs={'class': 'form-control'}),
        }