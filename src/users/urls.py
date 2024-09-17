from django.urls import path
from users.views import SignInAPIVIew, SignUpAPIVIew, SignOutAPIVIew, RefreshTokenAPIVIew, VerifyEmailView


urlpatterns = [
    path("sign_in/", SignInAPIVIew.as_view(), name='sign_in'),
    path("sign_up/", SignUpAPIVIew.as_view(), name='sign_up'),
    path("sign_out/", SignOutAPIVIew.as_view(), name='sign_out'),
    path("refresh/", RefreshTokenAPIVIew.as_view(), name='refresh_token'),
    path("verify/<str:token>", VerifyEmailView.as_view(), name='verify_email'),
]