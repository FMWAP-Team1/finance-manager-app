from django.db import models
from accounts.models import Account
from typing import Optional
from decimal import Decimal
from django.utils import timezone

class TransactionHistory(models.Model):
    account: Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount: Decimal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_after: Decimal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transaction_info: str = models.CharField(max_length=255)
    transaction_type: str = models.CharField(max_length=20)
    payment_type: str = models.CharField(max_length=20)
    transaction_dt: timezone.datetime = models.DateTimeField(auto_now_add=True)
    modified_dt: timezone.datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Transaction {self.id} for {self.account.account_num}"
