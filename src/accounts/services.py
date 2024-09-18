from django.db import transaction
from django.core.exceptions import ValidationError
from accounts.models import Account
import logging

logger = logging.getLogger(__name__)


class AccountService:
    @staticmethod
    def create_account(user, account_data):
        try:
            account = Account.objects.create(user=user, **account_data)
            logger.info(f"계좌 생성: 사용자 {user.id}의 계좌 {account.id}")
            return account
        except ValidationError as e:
            logger.error(f"계좌 생성 실패: 사용자 {user.id}, 오류: {str(e)}")
            raise

    @staticmethod
    def get_account_with_transactions(account_id, user):
        account = Account.objects.get(id=account_id, user=user)
        transactions = account.transactionhistory_set.all()
        return account, transactions

    @staticmethod
    def delete_account(account_id, user):
        account = Account.objects.get(id=account_id, user=user)
        account_id = account.id
        account.delete()
        logger.info(f"계좌 삭제: 사용자 {user.id}의 계좌 {account_id}")

    @staticmethod
    @transaction.atomic
    def perform_transaction(account, transaction_data):
        amount = transaction_data['amount']
        transaction_type = transaction_data['transaction_type']

        if transaction_type == 'withdraw' and account.balance < amount:
            raise ValidationError("잔액 부족으로 출금할 수 없습니다.")

        account.balance += amount if transaction_type == 'deposit' else -amount
        account.save()

        transaction = account.transactionhistory_set.create(**transaction_data)
        logger.info(f"거래 수행: 계좌 {account.id}, 거래 ID {transaction.id}")
        return account


class UserService:
    @staticmethod
    def get_user_with_accounts(user):
        accounts = user.account_set.all()
        return user, accounts