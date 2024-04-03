from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'InputEmail', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPassword'}))

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputFirstName'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputLastName'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'inputEmail4', 'placeholder': 'example@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPassword4', 'placeholder': 'Password'}))
    address = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputAddress', 'placeholder': '1234 Main St'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputPhoneNumber'}))
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPin', 'maxlength': '4'}))

class UploadCheckForm(forms.Form):
    check = forms.ImageField()
    account = forms.ChoiceField()
    amount = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputAmount', 'placeholder': '0.00'}))