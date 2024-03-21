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

    # first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputFirstName'}))
    # last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputLastName'}))
    # email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'inputEmail4', 'placeholder': 'example@gmail.com'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPassword4', 'placeholder': 'Password'}))
    # address = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputAddress', 'placeholder': '1234 Main St'}))
    # phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputPhoneNumber'}))
    # pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPin', 'maxlength': '4'}))