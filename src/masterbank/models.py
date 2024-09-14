from django.db import models
from typing import List

class MasterBank(models.Model):
    bank_code: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="은행 코드"
    )
    bank_name: models.CharField = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="은행 이름"
    )

    class Meta:
        verbose_name: str = "은행 정보"
        verbose_name_plural: str = "은행 정보들"
        indexes: List[models.Index] = [
            models.Index(fields=['bank_name'])
        ]

    def __str__(self) -> str:
        return f"{self.bank_name} ({self.bank_code})"
