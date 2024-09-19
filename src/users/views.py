import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

from accounts.pagination import StandardResultsSetPagination
from accounts.serializers import AccountDetailSerializer
from users.exceptions import InvalidTokenError, UserNotFoundError
from users.serializers import UserDetailSerializer
from users.services import (sign_up, sign_in, sign_out,
                            refresh_token,
                            verify_email,
                            UserService)
from utils.email import send_verification_email


class SignInAPIVIew(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            sign_in_result = sign_in(login_type="email", **request.data)
            response = Response(data={"message": "로그인에 성공하였습니다."}, status=status.HTTP_200_OK)

            response.set_cookie(
                key="access",
                value=sign_in_result.get("access"),
                httponly=True,
                secure=settings.SECURE_COOKIES,  # 배포 환경에서만 True로 설정
                samesite='Lax'
            )
            response.set_cookie(
                key="refresh",
                value=sign_in_result.get("refresh"),
                httponly=True,
                secure=settings.SECURE_COOKIES,
                samesite='Lax'
            )

            return response
        except ValidationError as ve:
            return Response(data={"error_message": ve.detail}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        kakao_oauth_url = (
            f"https://kauth.kakao.com/oauth/authorize?"
            f"client_id={settings.KAKAO_RESTAPI_KEY}&"
            f"redirect_uri={settings.KAKAO_REDIRECT_URI}&"
            f"response_type=code"
        )
        return redirect(kakao_oauth_url)


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 쿼리 파라미터에서 'code' 값 추출
        code = request.GET.get('code')

        # TODO: 리팩토링 필요
        # 액세스 토큰 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        token_data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_RESTAPI_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
        }
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        token_response = requests.post(token_url, data=token_data, headers=token_headers)
        token_json = token_response.json()

        if "error" in token_json:
            return Response({"error": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_json.get("access_token")

        # 사용자 정보 요청
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        user_info_headers = {
            "Authorization": f"Bearer {access_token}",
        }

        user_info_response = requests.get(user_info_url, headers=user_info_headers)
        user_info_json = user_info_response.json()

        kakao_account = user_info_json.get("kakao_account")

        # 사용자 정보로 로그인 처리 (여기서 유저 생성 또는 로그인 처리)
        # 예: 이메일로 사용자 식별
        email = kakao_account.get("email")
        _ = sign_up(email=email, login_type="kakao")
        sign_in_result = sign_in(email=email, login_type="kakao")
        response = Response(data={"message": "로그인에 성공하였습니다."}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access",
            value=sign_in_result.get("access"),
            httponly=True,
            secure=settings.SECURE_COOKIES,  # 배포 환경에서만 True로 설정
            samesite='Lax'
        )
        response.set_cookie(
            key="refresh",
            value=sign_in_result.get("refresh"),
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite='Lax'
        )

        return response


class SignUpAPIVIew(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            sign_up_result = sign_up(login_type="email", **request.data)
            send_verification_email(sign_up_result.get("email"))

            return Response(data=sign_up_result, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response(data={"error_message": ve.detail}, status=status.HTTP_400_BAD_REQUEST)


class SignOutAPIVIew(APIView):
    def get(self, request, *args, **kwargs):
        try:
            refresh = request.COOKIES.get("refresh")
            if refresh:
                sign_out(refresh)
        finally:
            response = Response(data={"message": "정상적으로 로그아웃 되었습니다."}, status=status.HTTP_200_OK)
            response.delete_cookie("access")
            response.delete_cookie("refresh")
            return response


class RefreshTokenAPIVIew(APIView):
    def get(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response(data={"error_message": "정상적인 토큰을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token_result = refresh_token(refresh)
        response = Response(data=refresh_token_result, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access",
            value=refresh_token_result.get("access"),
            httponly=True,
            secure=settings.SECURE_COOKIES,  # 배포 환경에서만 True로 설정
            samesite='Lax'
        )
        response.set_cookie(
            key="refresh",
            value=refresh_token_result.get("refresh"),
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite='Lax'
        )

        return response


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            verify_email_result = verify_email(token)
            return HttpResponse(f"<h1>{verify_email_result}</h1>", status=status.HTTP_200_OK)
        except ValidationError as ve:
            return HttpResponse(f"<h1>{ve.detail}</h1>", status=status.HTTP_400_BAD_REQUEST)
        except InvalidTokenError as ite:
            return HttpResponse(f"<h1>{ite.detail}</h1>", status=ite.status_code)
        except UserNotFoundError as unfe:
            return HttpResponse(f"<h1>{unfe.detail}</h1>", status=unfe.status_code)


class UserDetailAPIView(generics.RetrieveAPIView): #유저 쪽으로 분리
    permission_classes = [AllowAny]
    serializer_class = UserDetailSerializer
    pagination_class = StandardResultsSetPagination

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
