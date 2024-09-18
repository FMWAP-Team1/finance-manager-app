from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Account
from users.models import User
from .services import AccountService, UserService
from django.core.exceptions import ValidationError

class AccountServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass'
        )

    def test_create_account(self):
        account_data = {
            'account_number': '1234567890',
            'bank_code': 'ABC',
            'account_type': 'Savings'
        }
        account = AccountService.create_account(self.user, account_data)
        self.assertIsNotNone(account)
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.account_number, '1234567890')

    def test_perform_transaction(self):
        account = Account.objects.create(
            user=self.user, account_number='1234567890', bank_code='ABC', account_type='Savings', balance=100)
        transaction_data = {
            'amount': 50,
            'transaction_type': 'withdraw',
            'payment_type': 'card',
            'transaction_info': 'Test withdrawal'
        }
        updated_account = AccountService.perform_transaction(account, transaction_data)
        self.assertEqual(updated_account.balance, 50)

    def test_insufficient_funds(self):
        account = Account.objects.create(
            user=self.user, account_number='1234567890', bank_code='ABC', account_type='Savings', balance=100)
        transaction_data = {
            'amount': 150,
            'transaction_type': 'withdraw',
            'payment_type': 'card',
            'transaction_info': 'Test withdrawal'
        }
        with self.assertRaises(ValidationError):
            AccountService.perform_transaction(account, transaction_data)
