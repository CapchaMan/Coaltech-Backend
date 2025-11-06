from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Vendor, Rider

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class VendorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['business_name', 'business_address', 'business_phone', 'business_email', 'business_description']

class RiderRegistrationForm(forms.ModelForm):
    class Meta:
        model = Rider
        fields = ['phone_number', 'vehicle_type', 'vehicle_plate']
