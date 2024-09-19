from rest_framework import serializers
from transaction_history.models import TransactionHistory


class THListSerializer(serializers.ModelSerializer):
    """
    List를 조회하기 위한 Serializer를 여기에 정의해주세요
    """
    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'account',
            'amount',
            'balance_after',
            'transaction_info',
            'transaction_type',
            'created_dt'
        ]


class THCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = [
            'account',
            'amount',
            'balance_after',
            'transaction_info',
            'transaction_type',
            'payment_type',
        ]