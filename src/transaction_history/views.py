from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from transaction_history.models import TransactionHistory
from transaction_history.serializers import THListSerializer


class THListAPIView(APIView):
    """
        THListAPIView에서는 특정 계좌의 거래 내역을 조회하기 위한 API입니다.
    """

    def get(self, request, account_id):
        try:
            # 특정 계좌의 거래 내역 가져오기
            transactions = TransactionHistory.objects.filter(account__id=account_id)

            # 직렬화
            serializer = THListSerializer(transactions, many=True)

            # 응답 반환
            return Response(serializer.data, status=status.HTTP_200_OK)

        except TransactionHistory.DoesNotExist:
            return Response({"error": "거래 내역을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    