# accounts/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import Account
from .serializers import (
    AccountCreateSerializer,
    AccountDetailSerializer,
    AccountTransactionSerializer,
    UserDetailSerializer
)
from transaction_history.serializers import THListSerializer
from .permissions import IsAccountOwner
from .services import AccountService, UserService
from .pagination import StandardResultsSetPagination


class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            AccountService.create_account(self.request.user, serializer.validated_data)
        except ValidationError as e:
            return Response({'오류': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    pagination_class = StandardResultsSetPagination  # 페이지네이션 클래스 지정

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['account_id'], user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        account, transactions = AccountService.get_account_with_transactions(self.kwargs['account_id'], request.user)
        account_data = self.get_serializer(account).data

        paginator = self.pagination_class()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        transaction_data = THListSerializer(paginated_transactions, many=True).data

        return paginator.get_paginated_response({
            '계좌': account_data,
            '거래내역': transaction_data
        })

    def destroy(self, request, *args, **kwargs):
        AccountService.delete_account(self.kwargs['account_id'], request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountTransactionAPIView(generics.CreateAPIView):
    serializer_class = AccountTransactionSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        account = get_object_or_404(Account, id=self.kwargs['account_id'], user=self.request.user)
        try:
            AccountService.perform_transaction(account, serializer.validated_data)
        except ValidationError as e:
            return Response({'오류': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # 페이지네이션 클래스 지정

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user, accounts = UserService.get_user_with_accounts(request.user)
        user_data = self.get_serializer(user).data

        paginator = self.pagination_class()
        paginated_accounts = paginator.paginate_queryset(accounts, request)
        account_data = AccountDetailSerializer(paginated_accounts, many=True).data

        return paginator.get_paginated_response({
            '사용자': user_data,
            '계좌목록': account_data
        })