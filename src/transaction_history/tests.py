from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.utils import timezone
from accounts.models import Account
from masterbank.models import MasterBank
from transaction_history.models import TransactionHistory

User = get_user_model()

class TransactionHistoryModelTest(TestCase):
    def setUp(self):
        # 테스트에 필요한 사용자, 은행, 계좌 생성
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            nickname='testuser',
            name='Test User',
            phone_number='1234567890'
        )
        self.bank = MasterBank.objects.create(
            bank_code='001',
            bank_name='Test Bank'
        )
        self.account = Account.objects.create(
            user_id=self.user,  # 'user'를 'user_id'로 변경
            account_num='1234567890',
            bank_code=self.bank,
            account_type='Savings',
            balance=Decimal('1000.00')
        )

    # 나머지 테스트 메서드들은 그대로 유지
    ...

    def test_transaction_str_method(self):
        # Given
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=Decimal('100.00'),
            balance_after=Decimal('1100.00'),
            transaction_info="Withdrawal",
            transaction_type="WITHDRAWAL",
            payment_type="ATM"
        )

        # When
        result = str(transaction)

        # Then
        expected = f"Transaction {transaction.id} for {self.account.account_num}"
        self.assertEqual(result, expected)

    # 다른 테스트 메서드들도 동일하게 유지