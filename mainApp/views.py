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
                form.add_error(None, "Invalid email or password")
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
            pass
    else:
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

def atm_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pin = form.cleaned_data['pin']
            user = authenticate(request, email=email, pin=pin)
            
            if user is not None:
                login(request, user)
                # Redirect the user to the appropriate URL after successful login
                return redirect('ATM.html')  # Redirect to ATM.html
            else:
                # If authentication fails, add an error to the form
                form.add_error(None, "Invalid email or PIN")
    else:
        form = LoginForm()
    
    return render(request, 'atm_login.html', {'form': form})


def atm_page(request):
    return render(request, 'ATM.html')

#def withdrawal(request):
    if request.method == "POST":
        account_id = request.POST.get('account')
        withdrawal_amount = int(request.POST.get('withdrawal_amount'))

        # Retrieve the selected account
        account = Accounts.objects.get(pk=account_id)

        # Check if the withdrawal amount exceeds the available balance
        if withdrawal_amount > account.balance:
            # Display error message if the withdrawal amount is greater than the available balance
            messages.error(request, "Insufficient funds. Please enter a lower withdrawal amount.")
            return redirect('withdrawal')

        # Subtract withdrawal amount from the account balance
        account.balance -= withdrawal_amount
        account.save()

        # Redirect to a success page or another view
        return redirect('success_page')

    # Fetch user's accounts to populate the dropdown
    accounts = request.user.accounts.all()  # Assuming the user's accounts are related to the user model

    return render(request, 'withdrawal.html', {'accounts': accounts})





    
    
