from django.shortcuts import render
from .forms import LoginForm

# Create your views here.

def home(request):
    form = LoginForm()
    return render(request, 'home.html', {'form': form})

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



    
    