from django.db import models
from users.models import User
from masterbank.models import MasterBank
from typing import Optional
from decimal import Decimal
from django.utils import timezone
from django.conf import settings

class Account(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_num = models.CharField(max_length=20, unique=True, null=True, blank=True)
    bank_code = models.ForeignKey(MasterBank, to_field="bank_code", on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.account_num}"

    class Meta:
        app_label = 'accounts'