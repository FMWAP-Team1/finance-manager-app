from common.models import BaseModel
from .consts import BANK_CODE_CHOICES, ACCOUNT_TYPE_CHOICES
from django.conf import settings
from decimal import Decimal
from typing import Optional
from .consts import BANK_CODE_CHOICES, ACCOUNT_TYPE_CHOICES

class Account(BaseModel):
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="사용자",
    )
    account_number: Optional[str] = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name="계좌번호",
    )
    bank_code: str = models.CharField(
        max_length=50,
        choices=BANK_CODE_CHOICES,
        verbose_name="은행 코드",
    )
    account_type: str = models.CharField(
        max_length=100,
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name="계좌 종류",
    )
    balance: Decimal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="잔액",
    )

    class Meta:
        verbose_name = "계좌"
        verbose_name_plural = "계좌들"

    def __str__(self) -> str:
        return f"{self.user.email} - {self.account_number}"