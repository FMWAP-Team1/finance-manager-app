from rest_framework import serializers
from accounts.models import Account
from users.models import User
from django.core.validators import MinValueValidator


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'bank_code', 'account_type']

    def validate_account_number(self, value):
        if Account.objects.filter(account_number=value).exists():
            raise serializers.ValidationError("이미 존재하는 계좌번호입니다.")
        return value


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'bank_code', 'account_type', 'balance']
        read_only_fields = ['id', 'balance']


class AccountTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    transaction_type = serializers.ChoiceField(choices=['deposit', 'withdraw'])
    payment_type = serializers.CharField(max_length=20)
    transaction_info = serializers.CharField(max_length=255)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'nickname', 'phone_number']
        read_only_fields = ['id', 'email']