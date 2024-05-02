from django import forms
from django.forms import ModelForm
from .models import Users

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'pin', 'password', 'address', 'phone_number']

class ATMLoginForm(forms.Form):
    account_number = forms.CharField(label='Account Number', max_length=100, widget=forms.TextInput(attrs={'required': True}))
    pin = forms.CharField(label='PIN', widget=forms.PasswordInput(attrs={'required': True}))