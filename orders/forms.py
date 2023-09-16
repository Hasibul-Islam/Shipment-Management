from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'order_date', ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            
        }
