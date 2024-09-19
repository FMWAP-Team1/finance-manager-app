from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from accounts.models import Account
from accounts.serializers import (AccountCreateSerializer, AccountDetailSerializer, AccountTransactionSerializer)
from accounts.services.account_service import AccountService
from accounts.pagination import StandardResultsSetPagination
from transaction_history.serializers import THListSerializer


class AccountCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            account = AccountService.create_account(request.user, serializer.validated_data)
            return Response(AccountDetailSerializer(account).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': '계좌 생성 중 중복 오류가 발생했습니다.'}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(
                {'error': f'계좌 생성 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AccountDetailAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get_object(self, account_id, user):
        try:
            return Account.objects.get(id=account_id, user=user)
        except Account.DoesNotExist:
            raise NotFound(detail="요청한 계좌를 찾을 수 없습니다.")

    def get(self, request, account_id):
        try:
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
        except NotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'error': '이 계좌에 접근할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {'error': f'계좌 정보 조회 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, account_id):
        try:
            account = self.get_object(account_id, request.user)
            AccountService.delete_account(account.id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'error': '이 계좌를 삭제할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {'error': f'계좌 삭제 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AccountTransactionAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, account_id):
        try:
            account = get_object_or_404(Account, id=account_id, user=request.user)
            serializer = AccountTransactionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_account = AccountService.perform_transaction(account, serializer.validated_data)
            return Response({
                "message": "거래가 성공적으로 완료되었습니다.",
                "account_id": updated_account.id,
                "new_balance": updated_account.balance
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': f'거래 유효성 검사 실패: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response({'error': '요청한 계좌를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'error': '이 계좌로 거래를 수행할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {'error': f'거래 수행 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )