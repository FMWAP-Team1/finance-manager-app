from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from accounts.models import Account
from accounts.serializers import (AccountCreateSerializer, AccountDetailSerializer, AccountTransactionSerializer)
from accounts.permissions import IsAccountOwner
from accounts.services import (AccountService)
from accounts.pagination import StandardResultsSetPagination
from transaction_history.serializers import THListSerializer


class AccountCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = AccountService.create_account(request.user, serializer.validated_data)
                return Response(AccountDetailSerializer(account).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAccountOwner]
    pagination_class = StandardResultsSetPagination

    def get_object(self, account_id, user):
        return get_object_or_404(Account, id=account_id, user=user)

    def get(self, request, account_id):
        account = self.get_object(account_id, request.user)
        account_data = AccountDetailSerializer(account).data

        transactions = account.transactionhistory_set.all().order_by('-created_dt')
        paginator = self.pagination_class()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        transaction_data = THListSerializer(paginated_transactions, many=True).data

        return paginator.get_paginated_response({
            '계좌': account_data,
            '거래내역': transaction_data
        })

    def delete(self, request, account_id):
        account = self.get_object(account_id, request.user)
        AccountService.delete_account(account.id, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def post(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        serializer = AccountTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_account = AccountService.perform_transaction(account, serializer.validated_data)
                return Response({
                    "message": "Transaction completed successfully.",
                    "account_id": updated_account.id,
                    "new_balance": updated_account.balance
                }, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)