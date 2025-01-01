from django import forms
from .models import Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'photo',
            'cust_name',
            'cust_gender',
            'cust_houseno',
            'cust_city',
            'cust_district',
            'cust_pincode',
            'cust_email',
            'cust_phno',
        ]
        widgets = {
            'cust_gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'cust_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cust_phno': forms.TextInput(attrs={'class': 'form-control'}),
        }
