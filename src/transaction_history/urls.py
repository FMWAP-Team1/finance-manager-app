from django.urls import path
from transaction_history.views import THListAPIView


# 선언된 APIView에서 가져가야할 적절한 path를 작성해주세요
# 해당 path를 작성한 후 djangoProject의 urls.py에 해당 urls를 include 해주세요
urlpatterns = [
    path("api/transactions/<int:account_id>/", THListAPIView.as_view(), name='transaction_history_list')
]
