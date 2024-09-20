from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from . middlewares import auth, guest
from .forms import BankAccountForm, BillPaymentForm
from .models import BankAccount, Transaction
from decimal import Decimal


# Create your views here.
@guest
def register_view(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'','password1':'','password2':''}
        form =UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html', {'form':form})
        
@guest
def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'','password':''}
        form =UserCreationForm(initial=initial_data)
    return render(request, 'auth/login.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('login')

@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')


def manage_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Link the account to the logged-in user
            account.save()
            return redirect('manage_account')
    else:
        form = BankAccountForm()
    
    # Display user's accounts
    user_accounts = BankAccount.objects.filter(user=request.user)
    
    return render(request, 'manage_account.html', {'form': form, 'accounts': user_accounts})


def edit_account(request, id):
    account = get_object_or_404(BankAccount, id=id, user=request.user)
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('manage_account')
    else:
        form = BankAccountForm(instance=account)
    
    return render(request, 'edit_account.html', {'form': form})


def delete_account(request, account_id):
    if request.method == "POST":
        # Fetch the account based on the account_id
        account = get_object_or_404(BankAccount, id=account_id, user=request.user)
        
        # Delete the account
        account.delete()
        
        # Display success message
        messages.success(request, "Bank account deleted successfully!")
        
        # Redirect to the manage account page
        return redirect('manage_account')
    
    # If the request method is GET, return an appropriate response (e.g., redirect to the manage account page)
    return redirect('manage_account')


@login_required
def check_balance(request):
    if request.method == 'POST':
        account_id = request.POST.get('account')
        bank_pin = request.POST.get('bank_pin')
        
        try:
            account = BankAccount.objects.get(id=account_id, user=request.user)
            if account.bank_pin == bank_pin:
                return render(request, 'check_balance_result.html', {'account': account})
            else:
                return render(request, 'check_balance.html', {'error': 'Invalid PIN'})
        except BankAccount.DoesNotExist:
            return render(request, 'check_balance.html', {'error': 'Account not found'})
    
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'check_balance.html', {'accounts': accounts})


def bank_transfer(request):
    if request.method == 'POST':
        sender_account_id = request.POST.get('sender_account')
        recipient_account_number = request.POST.get('recipient_account')
        amount = request.POST.get('amount')
        bank_pin = request.POST.get('bank_pin')

        try:
            sender_account = BankAccount.objects.get(id=sender_account_id, user=request.user)
        except BankAccount.DoesNotExist:
            messages.error(request, 'Sender account not found.')
            return redirect('bank_transfer')

        try:
            recipient_account = BankAccount.objects.get(account_number=recipient_account_number)
        except BankAccount.DoesNotExist:
            messages.error(request, 'Recipient account not found.')
            return redirect('bank_transfer')

        # Convert the amount to Decimal
        amount = Decimal(amount)

        if sender_account.bank_pin == bank_pin and sender_account.balance >= amount:
            # Deduct amount from sender
            sender_account.balance -= amount
            sender_account.save()

            # Add amount to recipient
            recipient_account.balance += amount
            recipient_account.save()

            # Create transaction records for both sender and receiver
            Transaction.objects.create(
                sender=sender_account.user,
                receiver=recipient_account.user,
                amount=amount,
                transaction_type='Debited',
            )
            Transaction.objects.create(
                sender=recipient_account.user,
                receiver=sender_account.user,
                amount=amount,
                transaction_type='Credited',
            )

            messages.success(request, 'Transfer successful!')
            return redirect('transaction_history')

        else:
            messages.error(request, 'Invalid PIN or insufficient funds.')
            return redirect('bank_transfer')

    return render(request, 'bank_transfer.html')


@login_required
def bill_payment(request):
    if request.method == 'POST':
        form = BillPaymentForm(request.user, request.POST)  # Pass the user
        if form.is_valid():
            bill_number = form.cleaned_data['bill_number']
            amount = form.cleaned_data['amount']
            account = form.cleaned_data['account']

            # Check if user owns the account
            if account.user == request.user and account.balance >= amount:
                # Deduct amount from the selected account
                account.balance -= amount
                account.save()

                # Record the bill payment transaction
                Transaction.objects.create(
                    sender=request.user,
                    receiver=None,  # Bill payment doesn't have a receiver
                    transaction_type='Bill Payment',
                    amount=amount,
                    bill_number=bill_number
                )

                return redirect('transaction_history')
            else:
                messages.error(request, 'Insufficient funds or unauthorized account.')
                return redirect('bill_payment')
    else:
        form = BillPaymentForm(user=request.user)  # Pass the user

    return render(request, 'bill_payment.html', {'form': form})


def submit_payment(request):
    if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_number = form.cleaned_data['bill_number']
            amount = form.cleaned_data['amount']
            account = form.cleaned_data['account']
            bank_pin = form.cleaned_data['bank_pin']

            # Check if the entered PIN is correct
            if account.bank_pin == bank_pin:  # Assuming 'bank_pin' is a field in your BankAccount model
                # Deduct the amount from the account and process the payment
                if account.balance >= amount:  # Ensure sufficient balance
                    account.balance -= amount
                    account.save()
                    messages.success(request, 'Payment submitted successfully.')
                    return redirect('success_page')  # Redirect to a success page
                else:
                    messages.error(request, 'Insufficient balance.')
            else:
                messages.error(request, 'Incorrect PIN. Please try again.')

    else:
        form = BillPaymentForm()
    return render(request, 'submit_payment.html', {'form': form})


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'transaction_history.html', {'transactions': transactions})
