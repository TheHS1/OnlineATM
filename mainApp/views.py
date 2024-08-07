from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import HttpResponse
from django_otp import devices_for_user, login as verifyOTP
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.db.models import Sum, Avg
from .forms import *
from .models import *
from .admin import *
import decimal

from .tasks import *

# For generating otp qr codes
import qrcode
from io import BytesIO
from base64 import b64encode

# Create your views here.

def otp_verify(request):
    devices = devices_for_user(request.user, confirmed=None)
    if request.method == "POST":
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
    # Check if the user has a registered otp device
    hasDevice = False;
    for device in devices:
        if isinstance(device, TOTPDevice):
            hasDevice = True
    if hasDevice:
        form = OtpForm()
        return render(request, 'home.html', {'form': form, 'title': 'Verify your identity',})
    return redirect(otp_register)


def home(request):
    if request.method == "POST":
        hasDevice = False
        form = LoginForm(request.POST)

        # login user if valid
        if form.is_valid():
            emailLogin = form.cleaned_data['email']
            passwordLogin = form.cleaned_data['password']
            user = authenticate(request, email=emailLogin, password=passwordLogin)
            
            if user is not None:
                login(request, user)
                return redirect(otp_verify)
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
            return render(request, 'register_view.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register_view.html', {'form': form})

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
        form.fields['account'].queryset = Accounts.objects.filter(user_id = request.user, is_deleted=False)
        if form.is_valid():
            dest = form.cleaned_data["account"]
            amt = form.cleaned_data["amount"]

            checkTransaction = form.save()
            transaction = Transactions.objects.create(destination=dest, amount=amt)
            transaction.save()

            checkTransaction.transaction = transaction
            checkTransaction.save()
            procCheck.delay_on_commit(checkTransaction.id, checkTransaction.front.path)

            messages.success(request, "Check submitted. Your transaction is currently under review")

            return redirect("confirm")

    form = UploadCheckForm()
    form.fields['account'].queryset = Accounts.objects.filter(user_id = request.user, is_deleted=False)
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
    transactions = Transactions.objects.filter(source__in=user_accounts, error=False) | Transactions.objects.filter(destination__in=user_accounts, error=False)
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
    accounts = Accounts.objects.filter(user_id=request.user, is_deleted=False)
    return render(request, 'accounts_view.html', {'form': form, 'accounts': accounts})

@otp_required
def confirm_account_deletion(request):
    if request.method == "POST":
        account_id = request.POST.get('account_id')
        if account_id:
            account = Accounts.objects.filter(id=account_id, user_id=request.user).first()
            if account:
                if account.balance == 0.0:
                    account.is_deleted = True
                    account.save()
                    messages.success(request, "Account closed successfully.")
                    return redirect('confirm')
                else: 
                    messages.error(request, "Only accounts with a balance of 0 can be deleted.")
                    return redirect('confirm')
            else:
                messages.error(request, "Account not found.")
                return redirect('confirm')
        else:
            messages.error(request, "No account selected for deletion.")
            return redirect('confirm')
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
        form.fields['account1'].queryset = Accounts.objects.filter(user_id = request.user, is_deleted=False)
        form.fields['account2'].queryset = Accounts.objects.filter(user_id = request.user, is_deleted=False)
        if form.is_valid():
            srce = form.cleaned_data["account1"] # account money taken from
            dest = form.cleaned_data["account2"] # account getting money
            amt = form.cleaned_data["amount"]
            if srce == dest:
                messages.error(request, "Source and destination must be different accounts")
            elif amt < 0:
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
    form.fields['account1'].queryset = Accounts.objects.filter(user_id = request.user, is_deleted=False)
    form.fields['account2'].queryset = Accounts.objects.filter(user_id = request.user, is_deleted=False)
    return render(request, 'transfer_funds.html', {"form": form})

def atm_login(request):
    if request.method == "POST":
        form = ATMLoginForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            pin = form.cleaned_data['pin']
            # Assuming Accounts model has fields 'account_number' and 'pin'
            
            account = Accounts.objects.filter(id=account_number).first()
            if account and account.user_id.pin == pin:
                # Redirect the user to the appropriate URL after successful login
                return redirect('atm_page', account_id=account_number)  # Redirect to the ATM page
            else:
                # If authentication fails, add an error to the form
                form.add_error(None, "Invalid account number or PIN")

    form = ATMLoginForm()
    return render(request, 'atm_login.html', {'form': form})

# @login_required
def atm_page(request, account_id):
    account = Accounts.objects.get(id=account_id)
    if request.method == "POST":
        # if 'withdrawal' in request.POST:
        # account_id = request.POST.get('account')
        withdrawal_amount = request.POST.get('withdrawal')
        try:
            # Convert withdrawal_amount to a decimal to ensure correct subtraction
            withdrawal_amount = decimal.Decimal(withdrawal_amount)

            if withdrawal_amount <= 0:
                messages.error(request, "Withdrawal amount must be greater than zero.")
                return redirect('atm_page', account_id=account_id)

            if withdrawal_amount > account.balance:
                messages.error(request, "Insufficient funds.")
                return redirect('atm_page', account_id=account_id)

            transaction = Transactions.objects.create(source=account, amount=withdrawal_amount)
            account.balance -= withdrawal_amount
            account.save()

            return redirect('withdraw_success')

        except decimal.InvalidOperation:
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('atm_page', account_id=account_id)

        
    # accounts = request.user.accounts.all()
    return render(request, 'atm_page.html', {"account": account})


def withdraw_success(request):
    return render(request, 'withdraw_success.html')

@otp_required
def admin_view(request):
    if request.user.is_superuser:
        return render(request, 'admin_view.html')
    
def admin_transaction_history(request):
    transactions = Transactions.objects.filter(error=False)
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
    accounts_within_range = Accounts.objects.none()
    users_within_range = Users.objects.none()
    deleted_accounts_within_range = Accounts.objects.none()

    total_amount_in_bank = Accounts.objects.filter(is_deleted=False).aggregate(total=Sum('balance'))['total'] or 0
    average_balance = Accounts.objects.filter(is_deleted=False).aggregate(average=Avg('balance'))['average'] or 0
    total_by_account_type = Accounts.objects.filter(is_deleted=False).values('account_type').annotate(total=Sum('balance'))

    if request.method == "POST" and form.is_valid():
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            accounts_within_range = Accounts.objects.filter(date_opened__gte=start_date, date_opened__lte=end_date)
            users_within_range = Users.objects.filter(date_opened__gte=start_date, date_opened__lte=end_date, is_superuser=False)
            deleted_accounts_within_range = Accounts.objects.filter(date_opened__gte=start_date, date_opened__lte=end_date, is_deleted=True)
    
    return render(request, 'bank_reports.html', {'form': form, 'accounts_within_range': accounts_within_range, 
                                                 'users_within_range': users_within_range, 
                                                 'deleted_accounts_within_range': deleted_accounts_within_range, 
                                                 'total_amount_in_bank': total_amount_in_bank,
                                                 'average_balance': average_balance,
                                                 'total_by_account_type': total_by_account_type})

def check_verification(request):
    transactions = Transactions.objects.filter(error=True)
    checks = checkTransactions.objects.filter(transaction__error=True)
    try:
        if request.method == "POST":
            transaction_id = request.POST.get('checkTransaction_id')

            transaction = Transactions.objects.get(id=transaction_id)
            checkTransaction = checkTransactions.objects.get(transaction=transaction)

            if 'AuthButton' in request.POST:
                print("Authed")
                amt = transaction.amount
                sender = transaction.source
                dest = transaction.destination
                print(amt)
                print(sender)
                print(dest)

                sender.balance -= amt
                dest.balance += amt
                transaction.error = False

                sender.save()
                dest.save()
                transaction.save()
            elif 'CancelButton' in request.POST:       
                print("BOOM") 
                checkTransaction.delete()
                transaction.delete()
    except:
        pass

    return render(request, 'check_verification.html', {'checkTransactions': checks})
