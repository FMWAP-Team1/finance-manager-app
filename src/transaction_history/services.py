from decimal import Decimal

from transaction_history.models import TransactionHistory


def add_transaction_history(account, amount: Decimal, balance_after: Decimal, transaction_info: str, transaction_type: str, payment_type: str):
    # Transaction History를 추가할 수 있도록 함수의 파라미터와 내부 로직을 수정 및 구현해주세요
    # Accounts View에서 거래를 생성했을 떄, 해당 메서드를 가져와서 DB에 transaction_history를 추가할 수 있도록 해주세요
    transaction_history = TransactionHistory(
        account=account,
        amount=amount,
        balance_after=balance_after,
        transaction_info=transaction_info,
        transaction_type=transaction_type,
        payment_type=payment_type
    )

    # DB에 저장
    transaction_history.save()
