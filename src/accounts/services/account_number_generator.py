import random
import string
from django.core.exceptions import ValidationError
from accounts.models import Account
from accounts.services.consts import BANK_PREFIXES, MAX_ATTEMPTS


class AccountNumberGenerator:
    @classmethod
    def generate(cls, bank_code):
        prefix = BANK_PREFIXES.get(bank_code, 'UK')
        for _ in range(MAX_ATTEMPTS):
            number = ''.join(random.choices(string.digits, k=13))
            account_number = f"{prefix}_{number}"
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number
        raise ValidationError("계좌번호를 생성할 수 없습니다.")