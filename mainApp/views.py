<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django_otp import devices_for_user, login as verifyOTP
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import *
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from .models import Accounts
=======
=======
from .models import Accounts, Transactions

>>>>>>> 235719b (Insert transaction into database)
from scripts import processCheck
>>>>>>> a4edfb3 (Add processing for check into deposit_view)
# from django.forms import Form
<<<<<<< HEAD
=======

# For generating otp qr codes
import qrcode
from io import BytesIO
from base64 import b64encode
>>>>>>> 831d31d (Implement OTP for users)
=======
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .forms import RegisterForm
from .forms import UploadCheckForm 
>>>>>>> f1c00da (created deposit page and image upload form without styling)
=======
from .models import *
>>>>>>> f18bf0b (Added transaction_history view and html page)

# Create your views here.

def home(request):
    if request.method == "POST":
        devices = devices_for_user(request.user, confirmed=None)

        # check if otp form was submitted or normal login form
        if ('verify' in request.POST):
            form = OtpForm(request.POST)

            # check if submitted token matches device token
            if form.is_valid():
                token = form.cleaned_data['otp_token']
                for device in devices:
                    if isinstance(device, TOTPDevice) and device.verify_token(token):
                        if device.confirmed == False:
                            device.confirmed = True;
                            device.save()
                        verifyOTP(request, device)
                        return redirect('customer_view')
                error_message = "Incorrect OTP code"
                form = OtpForm()
                return render(request, 'home.html', {'form': form, 'title': 'Verify your identity', 'error_message': error_message})
        else:
            hasDevice = False
            form = LoginForm(request.POST)

            # login user if valid
            if form.is_valid():
                emailLogin = form.cleaned_data['email']
                passwordLogin = form.cleaned_data['password']

                user = authenticate(request, email=emailLogin, password=passwordLogin)
                
                if user is not None:
                    login(request, user)
                    # Check if the user has a registered otp device
                    for device in devices:
                        if isinstance(device, TOTPDevice):
                            hasDevice = True
                    if hasDevice:
                        form = OtpForm()
                        return render(request, 'home.html', {'form': form, 'title': 'Verify your identity'})
                    return redirect(otp_register)
                else:
                    error_message = "Invalid username or password."
                return render(request, 'home.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
        if request.user.is_verified():
            return redirect('customer_view')
    return render(request, 'home.html', {'form': form})

@login_required
def otp_register(request):
    devices = devices_for_user(request.user, confirmed=None)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return redirect('home')

    device = request.user.totpdevice_set.create(confirmed=False)
    url = device.config_url
    qr_code_img = qrcode.make(device.config_url)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64, {encoded_img}'
    return render(request, 'otp_register.html', {'url': url, 'qrcode': qr_code_data})

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
        if (form.is_valid()) and (form.cleaned_data['password2'] == form.cleaned_data['password3']):
            emailLogin = form.cleaned_data['email']
            passwordLogin = form.cleaned_data['password1']
            pinLogin = form.cleaned_data['pin']
            user = authenticate(request, email=emailLogin, password=passwordLogin, pin=pinLogin)
            
            if (user is not None):
                user.set_password(form.cleaned_data["password2"])
                user.save()
            else:
                error_message = "Account does not exist."
                return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
            return redirect('home')
        
        elif ((form.cleaned_data['password2'] != form.cleaned_data['password3'])):
            error_message = "Passwords do not match"
            return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
        
        else:
            error_message = "Invalid email or pin"
            return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
    else:
        form = ResetForm()

    return render(request, 'reset_password.html', {'form': form})

@otp_required
def customer_view(request):
    return render(request, 'customer_view.html')

@otp_required
def deposit_view(request):
<<<<<<< HEAD
    if request.method == "POST":
        form = UploadCheckForm(request.POST, request.FILES)
        if form.is_valid():
<<<<<<< HEAD
            transaction = form.save()
            processCheck.getCheckInfo(transaction.front.path)
    else:
        form = UploadCheckForm()
=======
            dest = form.cleaned_data["account"]
            amt = form.cleaned_data["amount"]
            checkTransaction = form.save()
            processCheck.getCheckInfo(checkTransaction.front.path)
            transaction = Transactions.objects.create(destination=dest, source=dest, amount=amt)
            messages.success(request, "Check deposited Successfully.")
            return redirect("confirm")
            pass
>>>>>>> 235719b (Insert transaction into database)

    return render(request, 'deposit_view.html', {"form": form})
=======
    form = UploadCheckForm(request.POST, request.FILES)
    form.fields['account'].queryset = Accounts.objects.filter(user_id = request.user)
    return render(request, 'deposit_view.html', {'form': form})
>>>>>>> 96ff81d (Show accounts choice on page)

@otp_required
def user_settings(request):
    return render(request, 'user_settings.html')

@otp_required
def transaction_history(request):

    user_accounts = Accounts.objects.filter(user_id=request.user)
    transactions = Transactions.objects.filter(source__in=user_accounts) | Transactions.objects.filter(destination__in=user_accounts)
    transactions = transactions.order_by('-timestamp')

    return render(request, 'transaction_history.html', {'transactions': transactions})

@otp_required
def accounts_view(request):
    if request.method == "POST":
        if 'delete' in request.POST and request.user.is_authenticated:
            account_id = request.POST['account_id']
            if Accounts.objects.filter(user_id=request.user, id=account_id).delete():
                messages.success(request, "Account closed successfully.")
                return redirect("confirm")
        elif 'add' in request.POST and request.user.is_authenticated:
            form = addAccountForm(request.POST)
            if form.is_valid():
                type = form.cleaned_data["accountType"]
                account = Accounts.objects.create(account_type=type, user_id=request.user)
                account.save()
                messages.success(request, "Account opened successfully.")
                return redirect("confirm")
        return redirect("accounts_view");

    form = addAccountForm()
    accounts = Accounts.objects.filter(user_id=request.user)
    return render(request, 'accounts_view.html', {'form': form, 'accounts': accounts})

def confirm(request):
    return render(request, 'confirmation.html')

@otp_required
def transfer_funds(request):
    return render(request, 'transfer_funds.html')
<<<<<<< HEAD
=======

>>>>>>> a4edfb3 (Add processing for check into deposit_view)
