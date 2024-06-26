from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import ResetForm

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('confirmation/', views.confirm, name='confirm'),
    path('confirm_account_deletion/', views.confirm_account_deletion, name='confirm_account_deletion'),
    path('otp_register/', views.otp_register, name='otp_register'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('customer_view/', views.customer_view, name='customer_view'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('deposit_view/', views.deposit_view, name='deposit_view'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('user_settings/password/', views.user_settings_password, name='user_settings_password'),
    path('user_settings/pin/', views.user_settings_pin, name='user_settings_pin'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('accounts_view/', views.accounts_view, name='accounts_view'),
    path('transfer_funds/', views.transfer_funds, name='transfer_funds'),
    path('register_view/', views.register_view, name='register_view'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='pass_sent.html'), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='reset_password.html', form_class=ResetForm), 
         name='password_reset_confirm'),
    path('reset_password_success', auth_views.PasswordResetCompleteView.as_view(template_name='pass_success.html'), name='password_reset_complete'),
    path('atm_login/', views.atm_login, name='atm_login'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('admin_transaction_history/', views.admin_transaction_history, name='admin_transaction_history'),
    path('bank_reports/', views.bank_reports, name='bank_reports'),
    path('check_verification/', views.check_verification, name='check_verification'),
    path('atm_page/<int:account_id>/', views.atm_page, name='atm_page'),
    path('withdraw_success/', views.withdraw_success, name='withdraw_success'),
    path('accounts/login/', views.atm_login, name='accounts_login_redirect'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
