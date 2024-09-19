from django.urls import path
from accounts.views import (
    AccountCreateAPIView,
    AccountDetailAPIView,
    AccountTransactionAPIView,
)

urlpatterns = [
    path('create/', AccountCreateAPIView.as_view(), name='account_create'),
    path('<uuid:account_id>/', AccountDetailAPIView.as_view(), name='account_detail'),
    path('<uuid:account_id>/transaction/', AccountTransactionAPIView.as_view(), name='account_transaction'),
]
