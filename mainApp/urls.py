from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('confirmation/', views.confirm, name='confirm'),
    path('customer_view/', views.customer_view, name='customer_view'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('deposit_view/', views.deposit_view, name='deposit_view'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('accounts_view/', views.accounts_view, name='accounts_view'),
    path('transfer_funds/', views.transfer_funds, name='transfer_funds'),
    path('register_view/', views.register_view, name='register_view'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('admin_transaction_history/', views.admin_transaction_history, name='admin_transaction_history'),
    path('bank_reports/', views.bank_reports, name='bank_reports'),
    path('check_verification/', views.check_verification, name='check_verification'),
]

