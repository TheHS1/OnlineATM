from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from .forms import LoginForm
from .forms import RegisterForm
from .forms import ModelForm
from .forms import Users
# from django.forms import Form

# Create your views here.

def home(request):
    if request.method == "POST":
        print("test1")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("test2")
            emailLogin = form.cleaned_data['email']
            passwordLogin = form.cleaned_data['password']
            user = authenticate(request, email=emailLogin, password=passwordLogin)
            
            if user is not None:
                login(request, user)
                print("success")
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'home.html', {'form': form})

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)
        if form.is_valid():

            # data = form.cleaned_data
            # user_profile = Users(
            #     first_name=data['first_name'],
            #     last_name=data['last_name'],
            #     email=data['email'],
            #     password=data['password'],
            #     address=data['address'],
            #     pin=data['pin'],
            #     phone_number=data['phone_number'],
            # )
            # user_profile.save()
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        print("test4")
        form = RegisterForm()

    return render(request, 'register_view.html', {'form': form})

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





    
    
