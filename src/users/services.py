from typing import Dict, Any

from auth_token.models import Jwt
from users.models import User
from users.serializers import SignUpSerializer, SignInSerializer
from utils.email import verify_email_verification_token
from utils.common import assemble_kwargs


def sign_up(email: str, password: str = None, login_type: str = "email", **kwargs) -> Dict[str, Any]:
    is_active = True
    if login_type == "email":
        is_active = False

    data = assemble_kwargs(email=email, password=password, login_type=login_type, is_active=is_active, **kwargs)

    serializer = SignUpSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return {
        "email": user.email,
        "is_active": user.is_active
    }


def verify_email(token: str) -> str:
    email = verify_email_verification_token(token)
    User.activate_user(email)

    return "이메일이 정상적으로 인증되었습니다. 로그인을 수행해주세요."


def sign_in(email: str, password: str = None, login_type: str = "email", **kwargs) -> Dict[str, str]:
    if login_type in ["email", "admin"]:
        data = assemble_kwargs(email=email, password=password, **kwargs)

        serializer = SignInSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        auth_user = serializer.validated_data.get("user")
    else:
        auth_user = User.objects.get(email=email)

    token = Jwt.generate_token(auth_user)
    return token.token_dict


def sign_out(refresh: str) -> None:
    Jwt.revoke_token(refresh)


def refresh_token(refresh: str) -> Dict[str, str]:
    new_token = Jwt.refresh_token(refresh=refresh)
    return new_token.token_dict


