from django import forms
from .models import *
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from dashboard.forms import CustomModelForm
import re
from django.core.exceptions import ValidationError
from schedly.widgets import *

password_pattern =  '[A-Za-z0-9!@#$%^&*()_+=\-[\]{};:\'",.<>?/\\|]'

class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })

    def clean(self):
        password = self.cleaned_data.get("password")
        print(password,'password')
        confirm_password = self.cleaned_data.get("confirm_password")
        print(confirm_password, 'confirm_password')

        if len(password) < 8:
            raise forms.ValidationError("Password must be more than 8 characters.")

        if len(password) < 8:
            raise forms.ValidationError("Password must be more than 8 characters.")

        if not re.match(password_pattern, password):
            raise forms.ValidationError("Password must be a mix of letters, numbers & symbols (#?!@$%^&*-).")
    
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords doesn't match. Both passwords must be same.")
        return self.cleaned_data

class CustomUserRegistrationForm(CustomModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name','email', 'phone', "gender","date_of_birth","address","city","state","country","pincode",'role']#   , 'password1', 'password2'] #'height', 'weight',
        widgets = {
            # 'amenities':PreOptionModelSelect2MultipleWidget(
            #         search_fields=['name__icontains'],
            #         attrs={'data-placeholder': 'Select Amenities'}
            # ),
                'gender': s2forms.Select2Widget(
                        attrs={'data-placeholder': 'Select Gender'}
                ),   
            }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserRegistrationForm, self).__init__(*args, **kwargs)
        # Apply Bootstrap classes and placeholders to each form field
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Full Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Email'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Phone (Optional)'
        })
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'DOB (Optional)',
            "type":"date"
        })
        self.custom_field_class()


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data
