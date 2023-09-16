from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'gender',
            'size_chart',
            'color_chart',
            'region_chart',
            'fabric_description',
            'other_descriptions',
            'quantity',
            'unit_price',
            
        ]

    product_name = forms.ChoiceField(choices=Product.PRODUCT_CHOICES)
    gender = forms.ChoiceField(choices=Product.GENDER_CHOICES)
    size_chart = forms.ChoiceField(choices=Product.SIZE_CHOICES)
    color_chart = forms.ChoiceField(choices=Product.COLOR_CHOICES)
    region_chart = forms.ChoiceField(choices=Product.REGION_CHOICES)
    fabric_description = forms.CharField(widget=forms.Textarea)
    other_descriptions = forms.CharField(widget=forms.Textarea)
    quantity = forms.IntegerField(min_value=1)
    unit_price = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)
    

