from django.contrib.auth.models import User
from django.db import models
import random

# Create your models here.


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    account_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    account_type = models.CharField(max_length=10, choices=[('savings', 'Savings'), ('current', 'Current')])
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    bank_pin = models.CharField(max_length=6, default='000000')

    def __str__(self):
        return f"{self.account_number} - {self.full_name}"
    
    

def generate_transaction_id():
    return str(random.randint(100000, 999999))

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=6, unique=True, default=generate_transaction_id)
    timestamp = models.DateTimeField(auto_now_add=True)
    bill_number = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id}: {self.amount} from {self.sender_account} to {self.receiver or 'N/A'}"


    