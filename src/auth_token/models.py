from typing import Dict
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class Jwt:
    def __init__(self, access: str, refresh: str):
        self._access = access
        self._refresh = refresh

    @property
    def token_dict(self) -> Dict[str, str]:
        return {
            "access": self.access,
            "refresh": self.refresh
        }

    @property
    def access(self) -> str:
        return self._access

    @access.setter
    def access(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("access 토큰은 String 타입입니다.")
        self._access = value

    @property
    def refresh(self) -> str:
        return self._refresh

    @refresh.setter
    def refresh(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("refresh 토큰은 String 타입입니다.")
        self._refresh = value

    @staticmethod
    def generate_token(auth_user: User) -> "Jwt":
        refresh = RefreshToken.for_user(user=auth_user)
        return Jwt(
            access=str(refresh.access_token),
            refresh=str(refresh)
        )

    @staticmethod
    def refresh_token(refresh: str) -> "Jwt":
        # 내부적으로 TokenBackend를 거쳐 String -> Token으로 변환
        new_refresh = RefreshToken(refresh)
        return Jwt(
            access=str(new_refresh.access_token),
            refresh=str(new_refresh)
        )

    @staticmethod
    def revoke_token(refresh: str) -> None:
        old_token = RefreshToken(refresh)
        old_token.blacklist()
