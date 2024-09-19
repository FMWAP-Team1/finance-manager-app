import random
import string
from django.core.exceptions import ValidationError
from accounts.models import Account

class AccountNumberGenerator:
    BANK_PREFIXES = {
        'KAKAOBANK': 'KA', 'KOOKMIN': 'KB', 'NH': 'NH',
        'IBK': 'IB', 'WOORI': 'WR', 'SHINHAN': 'SH'
    }
    MAX_ATTEMPTS = 1000

    @classmethod
    def generate(cls, bank_code):
        prefix = cls.BANK_PREFIXES.get(bank_code, 'UK')
        for _ in range(cls.MAX_ATTEMPTS):
            number = ''.join(random.choices(string.digits, k=13))
            account_number = f"{prefix}_{number}"
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number
        raise ValidationError("계좌번호를 생성할 수 없습니다.")