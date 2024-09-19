from django.urls import path
from transaction_history.views import THListAPIView


urlpatterns = [
    path("<int:account_id>/", THListAPIView.as_view(), name='transaction_history_list')
]