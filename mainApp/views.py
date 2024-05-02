from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django_otp import devices_for_user, login as verifyOTP
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import *
from .models import *
import uuid

from scripts import processCheck

# For generating otp qr codes
import qrcode
from io import BytesIO
from base64 import b64encode

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
                        return redirect('reset_password')
                error_message = "Incorrect OTP code"
                form = OtpForm()
                return render(request, 'reset_password.html', {'form': form, 'title': 'Verify your identity', 'error_message': error_message})
        else:
            hasDevice = False
            form = ResetForm(request.POST)

            # login user if valid
            if form.is_valid() and form.cleaned_data["password2"] == form.cleaned_data["password3"]:
                emailLogin = form.cleaned_data['email']
                user = authenticate(request, email=emailLogin)
                
                if user is not None:
                    # Check if the user has a registered otp device
                    for device in devices:
                        if isinstance(device, TOTPDevice):
                            hasDevice = True
                    if hasDevice:
                        form = OtpForm()
                        return render(request, 'reset_password.html', {'form': form, 'title': 'Verify your identity'})
                    return redirect(otp_register)
                else:
                    error_message = "Invalid username or password."
                return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})     
    else:
        form = ResetForm()
        if request.user.is_verified():
            return redirect('reset_password')
    return render(request, 'reset_password.html', {'form': form})

@otp_required
def customer_view(request):
    return render(request, 'customer_view.html')

@otp_required
def logout_view(request):
    logout(request)
    messages.success(request, "Sucessfully logged out")
    return redirect('home')

@otp_required
def deposit_view(request):
    if request.method == "POST":
        form = UploadCheckForm(request.POST, request.FILES)
        form.fields['account'].queryset = Accounts.objects.filter(user_id = request.user)
        if form.is_valid():
            dest = form.cleaned_data["account"]
            amt = form.cleaned_data["amount"]

            checkTransaction = form.save()
            data = processCheck.getCheckInfo(checkTransaction.front.path)

            if all(value != '' for value in data.values()):
                senderID = uuid.UUID(data['sender_account'])
                sender = Accounts.objects.get(id=senderID)

                if float(data['numerical_amount']) == float(amt):
                    if sender.balance >= amt:
                        transaction = Transactions.objects.create(destination=dest, source=sender, amount=amt)
                        checkTransaction.transaction = transaction

                        sender.balance -= amt
                        dest.balance += amt

                        sender.save()
                        dest.save()
                        checkTransaction.save()

                        messages.success(request, "Check deposited successfully.")
                    else: 
                        checkTransaction.delete()
                        messages.error(request, "Source account has insufficient funds")

                else:
                    checkTransaction.delete()
                    messages.error(request, "Check amount does not match listed amount")
            else:
                checkTransaction.delete()
                messages.error(request, "Could not read check")

            return redirect("confirm")

    form = UploadCheckForm()
    form.fields['account'].queryset = Accounts.objects.filter(user_id = request.user)
    return render(request, 'deposit_view.html', {"form": form})

@otp_required
def user_settings(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('user_settings')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'user_settings.html', {'form': form})

def user_settings_password(request):
    if request.method == "POST":
        form = ShortResetForm(request.POST)
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
        else:
            print(form.errors)
            error_message = "Invalid email, password, or pin"
            return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
    else:
        form = ShortResetForm()
    return render(request, 'user_settings_password.html', {"form": form})

def user_settings_pin(request):
    if request.method == "POST":
        form = PinResetForm(request.POST)
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
        else:
            print(form.errors)
            error_message = "Invalid email, password, or pin"
            return render(request, 'reset_password.html', {'form': form, 'error_message': error_message})
    else:
        form = PinResetForm()
    return render(request, 'user_settings_pin.html', {"form": form})

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
        return redirect("accounts_view")

    form = addAccountForm()
    accounts = Accounts.objects.filter(user_id=request.user)
    return render(request, 'accounts_view.html', {'form': form, 'accounts': accounts})

def confirm(request):
    return render(request, 'confirmation.html')

    form = addAccountForm()
    accounts = Accounts.objects.filter(user_id=request.user)
    return render(request, 'accounts_view.html', {'form': form, 'accounts': accounts})

def confirm(request):
    return render(request, 'confirmation.html')

@otp_required
def transfer_funds(request):
    if request.method == "POST":
        form = TansferFundsForm(request.POST)
        form.fields['account1'].queryset = Accounts.objects.filter(user_id = request.user)
        form.fields['account2'].queryset = Accounts.objects.filter(user_id = request.user)
        if form.is_valid():
            srce = form.cleaned_data["account1"] # account money taken from
            dest = form.cleaned_data["account2"] # account getting money
            amt = form.cleaned_data["amount"]
            if amt < 0:
                messages.error(request, "Invalid input")
            elif srce.balance >= amt:
                srce.balance -= amt;
                dest.balance += amt;
                srce.save();
                dest.save();
                transaction = Transactions.objects.create(destination=dest, source=srce, amount=amt)
                messages.success(request, "Funds Transfered Successfully.")
            else:
                messages.error(request, "Insufficient funds")


            return redirect("confirm")

    form = TansferFundsForm()
    form.fields['account1'].queryset = Accounts.objects.filter(user_id = request.user)
    form.fields['account2'].queryset = Accounts.objects.filter(user_id = request.user)
    return render(request, 'transfer_funds.html', {"form": form})

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

def withdrawal(request):
    return render(request, 'atm_login.html')

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
