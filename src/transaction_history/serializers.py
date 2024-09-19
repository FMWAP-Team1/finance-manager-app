from rest_framework import serializers
from transaction_history.models import TransactionHistory


class THListSerializer(serializers.ModelSerializer):
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