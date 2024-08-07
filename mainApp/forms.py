from django import forms
from django.forms import ModelForm
from .models import Users
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import MinLengthValidator
from django.forms import ModelForm
from .models import checkTransactions
from datetime import date

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

class UploadCheckForm(ModelForm):
    account = forms.ModelChoiceField(queryset=None)
    amount = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputAmount', 'placeholder': '0.00'}))
    class Meta:
        model = checkTransactions
        fields = ["front"]

class TransferFundsForm(forms.Form):
    account1 = forms.ModelChoiceField(queryset=None)
    account2 = forms.ModelChoiceField(queryset=None)
    amount = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputAmount', 'placeholder': '0.00'}))

class ResetForm(forms.Form):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}))
    new_password2 = forms.CharField(label='Re-Enter New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password3'}))
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
    

class addAccountForm(forms.Form):
    accountType = forms.ChoiceField(label='AccountType', widget=forms.Select(attrs={'class': 'form-select', 'id': 'accountType'}), choices=accountOptions)

class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}))
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'aria-describedby': 'emailHelp'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'phone_number'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'address'}))

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}))
    password2 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}))
    password3 = forms.CharField(label='Re-Enter New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password3'}))

class PinResetForm(forms.Form):
    pin1 = forms.CharField(label='Old Pin', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pin1'}))
    pin2 = forms.CharField(label='New Pin', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pin2'}))
    pin3 = forms.CharField(label='Re-Enter New Pin', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pin3'}))

class ReportForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput( attrs={'type': 'date', 'class': 'form-control'}))
class ATMLoginForm(forms.Form):
    account_number = forms.CharField(label='Account Number', max_length=100, widget=forms.TextInput(attrs={'required': True}))
    pin = forms.CharField(label='PIN', widget=forms.PasswordInput(attrs={'required': True}))
