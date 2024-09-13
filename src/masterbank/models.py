from django.db import models

class MasterBank(models.Model):
    bank_code: str = models.CharField(max_length=10, unique=True)
    bank_name: str = models.CharField(max_length=100, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['bank_name'])
        ]

    def __str__(self) -> str:
        return f"{self.bank_name} ({self.bank_code})"
