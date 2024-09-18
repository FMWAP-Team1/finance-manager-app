from django.urls import path
from users.views import (SignInAPIVIew, SignUpAPIVIew, SignOutAPIVIew,
                         RefreshTokenAPIVIew, VerifyEmailView, KakaoLoginView, KakaoCallbackView)


urlpatterns = [
    path("sign_in/", SignInAPIVIew.as_view(), name='sign_in'),
    path("kakao/sign_in/", KakaoLoginView.as_view(), name='kakao_sign_in'),
    path("kakao/callback/", KakaoCallbackView.as_view(), name='kakao_callback'),
    path("sign_up/", SignUpAPIVIew.as_view(), name='sign_up'),
    path("sign_out/", SignOutAPIVIew.as_view(), name='sign_out'),
    path("refresh/", RefreshTokenAPIVIew.as_view(), name='refresh_token'),
    path("verify/<str:token>/", VerifyEmailView.as_view(), name='verify_email'),
]
