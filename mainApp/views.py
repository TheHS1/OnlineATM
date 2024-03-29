from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
# from django.forms import Form

# Create your views here.

def home(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            emailLogin = form.cleaned_data['email']
            passwordLogin = form.cleaned_data['password']
            user = authenticate(request, email=emailLogin, password=passwordLogin)
            
            if user is not None:
                login(request, user)
                return redirect('customer_view')
            else:
                error_message = "Invalid username or password."
                return render(request, 'home.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'home.html', {'form': form})

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('home')
        else:
            error_message = "Invalid credentials."
            return render(request, 'register_view.html', {'form': form, 'error_message': error_message})
    else:
        form = RegisterForm()

    return render(request, 'register_view.html', {'form': form})

def reset_password(request):

    if request.method == "POST":

        form = ResetForm(request.POST)
        print("test1")
        if (form.is_valid()) and (form.cleaned_data['password2'] == form.cleaned_data['password3']):
            print("test2")
            user = form.save(commit=False)
            emailLogin = form.cleaned_data['email']
            passwordLogin = form.cleaned_data['password1']
            pinLogin = form.cleaned_data['pin']
            user = authenticate(request, email=emailLogin, password=passwordLogin, pin=pinLogin)
            
            if (user is not None):
                user.set_password(form.cleaned_data["password2"])
            else:
                error_message = "Account does not exist."
                return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
            return redirect('home')
        else:
            error_message = "Invalid email, password, or pin"
            return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
    else:
        form = ResetForm()

    return render(request, 'reset_password.html', {'form': form})

def customer_view(request):
    return render(request, 'customer_view.html')

def deposit_view(request):
    return render(request, 'deposit_view.html')

def user_settings(request):
    return render(request, 'user_settings.html')

def transaction_history(request):
    return render(request, 'transaction_history.html')

def accounts_view(request):
    return render(request, 'accounts_view.html')

def transfer_funds(request):
    return render(request, 'transfer_funds.html')





    
    
