from django.urls import path
from accounts.views import (
    AccountCreateAPIView,
    AccountDetailAPIView,
    AccountTransactionAPIView,
    UserDetailAPIView
)

urlpatterns = [
    path('accounts/create/', AccountCreateAPIView.as_view(), name='account_create'),
    path('accounts/<uuid:account_id>/', AccountDetailAPIView.as_view(), name='account_detail'),
    path('accounts/<uuid:account_id>/transaction/', AccountTransactionAPIView.as_view(), name='account_transaction'),
    path('users/me/', UserDetailAPIView.as_view(), name='user_detail'),
]