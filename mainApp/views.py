from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from .models import Accounts
from django.contrib import messages
from .forms import ATMLoginForm


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
        form = ATMLoginForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            pin = form.cleaned_data['pin']
            # Assuming Accounts model has fields 'account_number' and 'pin'
            
            if Accounts.objects.get(id=account_number) and Users.objects.get(pin=pin):
                # Redirect the user to the appropriate URL after successful login
                return redirect('atm_page', account_id=account_number)  # Redirect to the ATM page
            else:
                # If authentication fails, add an error to the form
                form.add_error(None, "Invalid account number or PIN")
    else:
        form = ATMLoginForm()
    
    return render(request, 'atm_login.html', {'form': form})

# @login_required
def atm_page(request, account_id):
    if request.method == "POST":
        if 'withdrawal' in request.POST:
            # account_id = request.POST.get('account')
            withdrawal_amount = request.POST.get('withdrawal_amount')

            try:
                account = Accounts.objects.get(pk=account_id)

                # Validate withdrawal amount
                if not withdrawal_amount.isdigit() or int(withdrawal_amount) <= 0:
                    messages.error(request, "Withdrawal amount must be a positive integer.")
                    return redirect('atm_page')

                withdrawal_amount = int(withdrawal_amount)

                if withdrawal_amount > account.balance:
                    messages.error(request, "Insufficient funds. Please enter a lower withdrawal amount.")
                    return redirect('atm_page')

                account.balance -= withdrawal_amount
                account.save()

                return redirect('withdraw_success')

            except Accounts.DoesNotExist:
                messages.error(request, "Selected account does not exist.")
                return redirect('atm_page')

    # accounts = request.user.accounts.all()
    return render(request, 'ATM.html')


def withdraw_success(request):
    return render(request, 'withdraw_success.html')


