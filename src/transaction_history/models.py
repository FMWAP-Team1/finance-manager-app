from django.db import models
from decimal import Decimal
from datetime import datetime
from .consts import TRANSACTION_TYPE_CHOICES, TRANSACTION_INFO_CHOICES

class TransactionHistory(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="계좌")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="거래 금액")
    balance_after = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="거래 후 잔액")
    transaction_info = models.CharField(
        max_length=255,
        choices=TRANSACTION_INFO_CHOICES,
        verbose_name="거래 내용"
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="거래 유형"
    )
    payment_type = models.CharField(max_length=20, verbose_name="결제 방식")
    transaction_dt = models.DateTimeField('거래일시', auto_now_add=True)
    modified_dt = models.DateTimeField('수정일시', auto_now=True)

    class Meta:
        verbose_name = "거래 내역"
        verbose_name_plural = "거래 내역들"

    def __str__(self):
        return f"{self.account} - {self.get_transaction_type_display()} - {self.amount}"
