from django.db import models
from common.models import BaseModel
from accounts.models import Account
from decimal import Decimal
from datetime import datetime
from typing import Optional
from .consts import TRANSACTION_INFO_CHOICES, PAYMENT_METHOD_CHOICES


class TransactionHistory(BaseModel):
    account: models.ForeignKey = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="계좌"
    )
    amount: Decimal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="거래 금액",
    )
    balance_after: Decimal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="거래 후 잔액",
    )
    transaction_info: str = models.CharField(
        max_length=255,
        choices=TRANSACTION_INFO_CHOICES,  #  consts.py에 TRANSACTION_TYPE_CHOICES 이라고 설정 되어있어서 TRANSACTION_INFO_CHOICES수정필요
        verbose_name="거래 내용",
    )
    transaction_type: str = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="거래 유형",
    )
    payment_type: str = models.CharField(
        max_length=20,
        verbose_name="결제 방식",
    )

    class Meta:
        verbose_name = "거래 내역"
        verbose_name_plural = "거래 내역들"

    def __str__(self) -> str:
        return f"{self.account} - {self.get_transaction_type_display()} - {self.amount}"