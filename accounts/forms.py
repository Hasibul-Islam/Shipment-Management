from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

PRODUCT_GENDER_CHOICES = (
        ('A', 'Admin'),
        ('M', 'Manager'),
        
    )
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'password1', 'password2']
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
        
        
        return user
