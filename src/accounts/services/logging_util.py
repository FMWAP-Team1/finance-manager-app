import logging

logger = logging.getLogger(__name__)

class LoggingUtil:
    @staticmethod
    def log_account_creation(user_id, account_id):
        logger.info(f"계좌 생성: 사용자 {user_id}의 계좌 {account_id}")

    @staticmethod
    def log_account_deletion(user_id, account_id):
        logger.info(f"계좌 삭제: 사용자 {user_id}의 계좌 {account_id}")

    @staticmethod
    def log_transaction(account_id, transaction_id):
        logger.info(f"거래 수행: 계좌 {account_id}, 거래 ID {transaction_id}")