from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .forms import RegisterForm
from .forms import UploadCheckForm 

# Create your views here.

def home(request):
    form = LoginForm()
    return render(request, 'home.html', {'form': form})

def register_view(request):
    form = RegisterForm()
    return render(request, 'register_view.html', {'form':form})

def customer_view(request):
    return render(request, 'customer_view.html')

def deposit_view(request):
    form = UploadCheckForm(request.POST, request.FILES)
    return render(request, 'deposit_view.html', {"form": form})

def user_settings(request):
    return render(request, 'user_settings.html')

def transaction_history(request):
    return render(request, 'transaction_history.html')

def accounts_view(request):
    return render(request, 'accounts_view.html')

def transfer_funds(request):
    return render(request, 'transfer_funds.html')





    
    