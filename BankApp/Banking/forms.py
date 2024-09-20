from django import forms
from .models import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_number', 'full_name', 'phone_number', 'email', 'account_type', 'balance','bank_pin']


class BankTransferForm(forms.Form):
    sender_account = forms.ModelChoiceField(queryset=None, label="Select Your Account")
    recipient_account_number = forms.CharField(max_length=20, label="Recipient's Account Number")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    bank_pin = forms.CharField(max_length=6, widget=forms.PasswordInput, label="Bank Pin")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super(BankTransferForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['sender_account'].queryset = BankAccount.objects.filter(user=user)



class BillPaymentForm(forms.Form):
    bill_number = forms.CharField(label='Bill Number', max_length=100)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    account = forms.ModelChoiceField(queryset=BankAccount.objects.none())  
    bank_pin = forms.CharField(label='Bank PIN', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(user=user)  # Filter accounts for the logged-in user
