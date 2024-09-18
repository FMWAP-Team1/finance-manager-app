from rest_framework.views import APIView


class THListAPIView(APIView):
    """
        THListAPIView에서는 특정 계좌의 거래 내역을 조회하기 위한 API입니다.
    """

    def get(self, request):
        ...
    