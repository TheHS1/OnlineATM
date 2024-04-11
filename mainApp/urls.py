from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer_view/', views.customer_view, name='customer_view'),
    path('deposit_view/', views.deposit_view, name='deposit_view'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('accounts_view/', views.accounts_view, name='accounts_view'),
    path('transfer_funds/', views.transfer_funds, name='transfer_funds'),
    path('register_view/', views.register_view, name='register_view'),
    path('atm_login/', views.atm_login, name='atm_login'),
    path('ATM.html/', views.atm_page, name='ATM.html'),
    


]

