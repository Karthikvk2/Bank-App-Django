from django.http import HttpResponseRedirect
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('manage-account/', views.manage_account, name='manage_account'),
    path('manage-account/edit/<int:id>/', views.edit_account, name='edit_account'),
    path('manage-account/delete/<int:account_id>/', views.delete_account, name='delete_account'),
    path('bank-transfer/', views.bank_transfer, name='bank_transfer'),
    path('check-balance/', views.check_balance, name='check_balance'),
    path('bill-payment/', views.bill_payment, name='bill_payment'),
    path('transaction-history/',  views.transaction_history, name='transaction_history'),
    path('', lambda request: HttpResponseRedirect('login/')),
]
