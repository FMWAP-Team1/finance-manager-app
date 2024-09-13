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

    def test_create_transaction(self):
        # Given
        amount = Decimal('500.00')
        balance_after = self.account.balance + amount
        transaction_info = "Deposit"
        transaction_type = "DEPOSIT"
        payment_type = "CASH"

        # When
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=amount,
            balance_after=balance_after,
            transaction_info=transaction_info,
            transaction_type=transaction_type,
            payment_type=payment_type
        )

        # Then
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.amount, amount)
        self.assertEqual(transaction.balance_after, balance_after)
        self.assertEqual(transaction.transaction_info, transaction_info)
        self.assertEqual(transaction.transaction_type, transaction_type)
        self.assertEqual(transaction.payment_type, payment_type)
        self.assertIsNotNone(transaction.transaction_dt)
        self.assertIsNotNone(transaction.modified_dt)

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

    def test_transaction_history_ordering(self):
        # Given
        TransactionHistory.objects.create(
            account=self.account,
            amount=Decimal('100.00'),
            balance_after=Decimal('1100.00'),
            transaction_info="Deposit 1",
            transaction_type="DEPOSIT",
            payment_type="CASH"
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=Decimal('200.00'),
            balance_after=Decimal('1300.00'),
            transaction_info="Deposit 2",
            transaction_type="DEPOSIT",
            payment_type="CASH"
        )

        # When
        transactions = TransactionHistory.objects.all()

        # Then
        self.assertEqual(len(transactions), 2)
        self.assertTrue(transactions[0].transaction_dt <= transactions[1].transaction_dt)

    def test_transaction_with_negative_amount(self):
        # Given
        initial_balance = self.account.balance
        withdrawal_amount = Decimal('-300.00')

        # When
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=withdrawal_amount,
            balance_after=initial_balance + withdrawal_amount,
            transaction_info="Withdrawal",
            transaction_type="WITHDRAWAL",
            payment_type="CARD"
        )

        # Then
        self.assertEqual(transaction.amount, withdrawal_amount)
        self.assertEqual(transaction.balance_after, initial_balance + withdrawal_amount)

    def test_multiple_transactions_for_account(self):
        # Given
        initial_balance = self.account.balance

        # When
        TransactionHistory.objects.create(
            account=self.account,
            amount=Decimal('500.00'),
            balance_after=initial_balance + Decimal('500.00'),
            transaction_info="Deposit",
            transaction_type="DEPOSIT",
            payment_type="CASH"
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=Decimal('-200.00'),
            balance_after=initial_balance + Decimal('300.00'),
            transaction_info="Withdrawal",
            transaction_type="WITHDRAWAL",
            payment_type="ATM"
        )

        # Then
        transactions = TransactionHistory.objects.filter(account=self.account)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1].balance_after, initial_balance + Decimal('300.00'))