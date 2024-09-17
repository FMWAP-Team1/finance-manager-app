from django.conf import settings
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.exceptions import InvalidTokenError, UserNotFoundError
from users.services import (sign_up, sign_in, sign_out,
                            refresh_token,
                            verify_email)
from users.utils import send_verification_email


class SignInAPIVIew(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            sign_in_result = sign_in(**request.data)
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


class SignUpAPIVIew(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            sign_up_result = sign_up(**request.data)
            send_verification_email(email=sign_up_result.get("email"), request=request)
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
