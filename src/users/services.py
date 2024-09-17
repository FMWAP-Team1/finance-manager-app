from typing import Dict, Any

from users.models import Token, User
from users.serializers import SignUpSerializer, SignInSerializer
from users.utils import verify_email_verification_token


def sign_up(email: str, password: str, name: str, phone_number: str, **kwargs) -> Dict[str, Any]:
    data = get_serializer_input_data(email=email, password=password, name=name, phone_number=phone_number, is_active=False, **kwargs)

    serializer = SignUpSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return {
        "email": user.email,
        "name": user.name,
        "phone_number": user.phone_number,
        "is_active": user.is_active
    }


def verify_email(token: str) -> str:
    email = verify_email_verification_token(token)
    User.activate_user(email)

    return "이메일이 정상적으로 인증되었습니다. 로그인을 수행해주세요."


def sign_in(email: str, password: str, **kwargs) -> Dict[str, str]:
    data = get_serializer_input_data(email=email, password=password, **kwargs)

    serializer = SignInSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    auth_user = serializer.validated_data.get("user")

    token = Token.generate_token(auth_user)
    return token.token_dict


def sign_out(refresh: str) -> None:
    Token.revoke_token(refresh)


def refresh_token(refresh: str) -> Dict[str, str]:
    new_token = Token.refresh_token(refresh=refresh)
    return new_token.token_dict


def get_serializer_input_data(**kwargs):
    return kwargs
