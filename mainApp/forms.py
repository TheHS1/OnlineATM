from django import forms
from django.forms import ModelForm
from .models import Users

accountOptions = (('Checkings', 'Checkings'), 
                  ('Savings', 'Savings'), ('Business', 'Business'))

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))

class OtpForm(forms.Form):
    otp_token = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

class RegisterForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'phone_number'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'address'}))
    pin = forms.CharField(label='Pin', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pin'}))

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'pin', 'password', 'address', 'phone_number']

class ResetForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    pin = forms.CharField(label='Pin', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pin'}))
    password1 = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}))
    password2 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}))
    password3 = forms.CharField(label='Re-Enter New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password3'}))

class addAccountForm(forms.Form):
    accountType = forms.ChoiceField(label='AccountType', widget=forms.Select(attrs={'class': 'form-select', 'id': 'accountType'}), choices=accountOptions)
