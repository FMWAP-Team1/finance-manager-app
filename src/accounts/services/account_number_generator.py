import random
import string
from django.core.exceptions import ValidationError
from accounts.models import Account
from accounts.services.consts import BANK_PREFIXES, MAX_ATTEMPTS, ACCOUNT_NUMBER_LENGTH


class AccountNumberGenerator:
    @staticmethod
    def generate(bank_code):
        if bank_code not in BANK_PREFIXES:
            raise ValidationError(f"유효하지 않은 은행 코드입니다: {bank_code}")

        prefix = BANK_PREFIXES[bank_code]
        for _ in range(MAX_ATTEMPTS):
            number = ''.join(random.choices(string.digits, k=ACCOUNT_NUMBER_LENGTH))
            account_number = f"{prefix}_{number}"
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number
        raise ValidationError("계좌번호를 생성할 수 없습니다.")