from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'InputEmail', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPassword'}))