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
from .admin import *

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
                        if request.user.is_superuser:
                            return redirect('admin_view')
                        else:
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
            if request.user.is_superuser:
                return redirect('admin_view')
            else:
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
        print("1")
        # check if otp form was submitted or normal login form
        if ('verify' in request.POST):
            form = OtpForm(request.POST)
            print("2")
            # check if submitted token matches device token
            if form.is_valid():
                print("3")
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
            print("4")
            hasDevice = False
            form = ResetForm(request.POST)

            # login user if valid
            if form.is_valid() and form.cleaned_data["password2"] == form.cleaned_data["password3"]:
                print("5")
                emailLogin = form.cleaned_data['email']
                user = authenticate(request, email=emailLogin)
                
                if user is not None:
                    print("6")
                    user.password = form.cleaned_data["password2"]
                    user.save()
                    # Check if the user has a registered otp device
                    for device in devices:
                        if isinstance(device, TOTPDevice):
                            hasDevice = True
                    if hasDevice:
                        form = OtpForm()
                        return render(request, 'reset_password.html', {'form': form, 'title': 'Verify your identity'})
                    return redirect(otp_register)
                else:
                    print("7")
                    error_message = "Invalid email."
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
                sender_id = int(data['sender_account'])
                sender_info = data['sender_info']
                recorded_date = data['date']
                spelled_amount = data['spelled_amount']
                recipient = data['recipient']
                memo = data['memo']
                sender = Accounts.objects.get(id=sender_id)

                if float(data['numerical_amount']) == float(amt):
                    if sender.balance >= amt:
                        transaction = Transactions.objects.create(destination=dest, source=sender, amount=amt)
    # sender_info = models.CharField(max_length=100)
    # writeDate = models.TimeField(auto_now_add=False)
    # numericalAmount = models.CharField(max_length=100)
    # recipientName = models.CharField(max_length=50)
    # memo = models.CharField(max_length=100)
                        checkTransaction.transaction = transaction
                        checkTransaction.sender_info = sender_info
                        checkTransaction.spelled_amount = spelled_amount
                        checkTransaction.recipient_name = recipient
                        checkTransaction.memo = memo

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
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('confirm')
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, 'user_settings.html', {'form': form})

def user_settings_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if (form.is_valid()) and (form.cleaned_data['password2'] == form.cleaned_data['password3']):
            passwordLogin = form.cleaned_data['password1']
            user = authenticate(request, email=request.user.email, password=passwordLogin, pin=request.user.pin)
            
            if (user is not None):
                user.set_password(form.cleaned_data["password2"])
                user.save()
                messages.success(request, "Password changed successfully")
            else:
                error_message = "Incorrect Old Password"
                return render(request, 'user_settings_password.html', {'form': form, 'error_message': error_message})
            return redirect('confirm')
        else:
            print(form.errors)
            error_message = "Invalid password"
            return render(request, 'user_settings_password.html', {'form': form, 'error_message': error_message})
    else:
        form = PasswordResetForm()
    return render(request, 'user_settings_password.html', {"form": form})

def user_settings_pin(request):
    print(request.user.password)
    print(request.user.email)
    if request.method == "POST":
        form = PinResetForm(request.POST)
        if (form.is_valid()) and (form.cleaned_data['pin2'] == form.cleaned_data['pin3']):
            pinLogin = form.cleaned_data['pin1']
            if(request.user.is_authenticated and pinLogin == request.user.pin):
                request.user.pin = (form.cleaned_data["pin2"])
                request.user.save()
                messages.success(request, "Pin changed successfully")
            else:
                error_message = "Incorrect Old Pin"
                return render(request, 'user_settings_pin.html', {'form': form, 'error_message': error_message})
            return redirect('confirm')
        else:
            print(form.errors)
            error_message = "Invalid pin"
            return render(request, 'user_settings_pin.html', {'form': form, 'error_message': error_message})
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
    if request.method == "POST" and request.user.is_authenticated:
        if 'delete' in request.POST:
            request.session['account_id_to_delete'] = request.POST['account_id']
            return redirect("confirm_account_deletion")
        elif 'add' in request.POST:
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
@otp_required
def confirm_account_deletion(request):
    if request.method == "POST":
        account_id = request.POST.get('account_id')
        if account_id:
            account = Accounts.objects.filter(id=account_id, user_id=request.user).first()
            if account:
                account.delete()
                messages.success(request, "Account closed successfully.")
                return redirect('confirm')
            else:
                messages.error(request, "Account not found.")
        else:
            messages.error(request, "No account selected for deletion.")
        return redirect("accounts_view")
    else:
        return redirect('accounts_view')

def confirm(request):
    return render(request, 'confirmation.html')

    form = addAccountForm()
    accounts = Accounts.objects.filter(user_id=request.user)
    return render(request, 'accounts_view.html', {'form': form, 'accounts': accounts})

def confirm(request):
    return render(request, 'confirmation.html')

@otp_required
@otp_required
def transfer_funds(request):
    if request.method == "POST":
        form = TransferFundsForm(request.POST)
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

    form = TransferFundsForm()
    form.fields['account1'].queryset = Accounts.objects.filter(user_id = request.user)
    form.fields['account2'].queryset = Accounts.objects.filter(user_id = request.user)
    return render(request, 'transfer_funds.html', {"form": form})

@otp_required
def admin_view(request):
    if request.user.is_superuser:
        return render(request, 'admin_view.html')
    
def admin_transaction_history(request):
    return render(request, 'admin_transaction_history.html')

def bank_reports(request):
    return render(request, 'bank_reports.html')

def check_verification(request):
    return render(request, 'check_verification.html')

    form = TansferFundsForm()
    form.fields['account1'].queryset = Accounts.objects.filter(user_id = request.user)
    form.fields['account2'].queryset = Accounts.objects.filter(user_id = request.user)
    return render(request, 'transfer_funds.html', {"form": form})


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

def admin_view(request):
    if request.user.is_superuser:
        return render(request, 'admin_view.html')
    
def admin_transaction_history(request):
    transactions = Transactions.objects.all()
    transactions = transactions.order_by('-timestamp')
    try:
        if request.method == "POST":
            transaction_id = request.POST.get('transaction_id')
            transaction = Transactions.objects.get(id=transaction_id)

            amt = transaction.amount
            src = transaction.source
            dst = transaction.destination

            src.balance += amt
            dst.balance -= amt

            src.save()
            dst.save()

            transaction.delete()
    except:
        pass
        
    return render(request, 'admin_transaction_history.html', {'transactions': transactions})

def bank_reports(request):
    form = ReportForm(request.POST or None)
    accounts_within_range = None
    users_within_range = None

    if request.method == "POST":
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            accounts_within_range = Accounts.objects.filter(date_opened__gte=start_date, date_opened__lte=end_date)
            users_within_range = Users.objects.filter(date_opened__gte=start_date, date_opened__lte=end_date)

    
    return render(request, 'bank_reports.html', {'form': form, 'accounts_within_range': accounts_within_range, 'users_within_range': users_within_range})

def check_verification(request):
    return render(request, 'check_verification.html')
