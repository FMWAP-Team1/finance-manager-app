from decimal import Decimal
from transaction_history.models import TransactionHistory
from transaction_history.serializers import THCreateSerializer


def add_transaction_history(account, amount: Decimal, balance_after: Decimal, transaction_info: str, transaction_type: str, payment_type: str):
    data = {
        'account': account.id,
        'amount': amount,
        'balance_after': balance_after,
        'transaction_info': transaction_info,
        'transaction_type': transaction_type,
        'payment_type': payment_type,
    }

    serializer = THCreateSerializer(data=data)

    # 유효성 검사
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValueError(serializer.errors)

