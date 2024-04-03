from django import forms
<<<<<<< HEAD
from django.forms import ModelForm
from .models import Users

accountOptions = (('Checkings', 'Checkings'), 
                  ('Savings', 'Savings'), ('Business', 'Business'))
=======
from django.core.files.uploadedfile import SimpleUploadedFile
<<<<<<< HEAD
>>>>>>> f1c00da (created deposit page and image upload form without styling)
=======
from django.forms import ModelForm
from .models import checkTransactions
>>>>>>> 0134aa4 (Create transaction model and update form)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))

<<<<<<< HEAD
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

<<<<<<< HEAD
class ResetForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    pin = forms.CharField(label='Pin', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pin'}))
    password1 = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}))
    password2 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}))
    password3 = forms.CharField(label='Re-Enter New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password3'}))
<<<<<<< HEAD

class addAccountForm(forms.Form):
    accountType = forms.ChoiceField(label='AccountType', widget=forms.Select(attrs={'class': 'form-select', 'id': 'accountType'}), choices=accountOptions)
=======
>>>>>>> 831d31d (Implement OTP for users)
=======
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
<<<<<<< HEAD
>>>>>>> f1c00da (created deposit page and image upload form without styling)
=======
class UploadCheckForm(ModelForm):
    class Meta:
        model = checkTransactions
        fields = ["front"]
>>>>>>> 0134aa4 (Create transaction model and update form)
=======
    account = forms.ChoiceField()
    amount = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputAmount', 'placeholder': '0.00'}))
>>>>>>> 8f52a6f (added amount and account entries to deposit form, as well as confirmation warning)
