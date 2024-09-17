from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Optional, Any, List, Dict

from users.managers import UserManager
from users.exceptions import UserNotFoundError
from common.models import BaseModel



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email: models.EmailField = models.EmailField(
        unique=True,
        verbose_name="이메일"
    )
    password: models.CharField = models.CharField(
        max_length=100,
        verbose_name="비밀번호"
    )
    name: models.CharField = models.CharField(
        max_length=100,
        verbose_name="이름"
    )
    nickname: models.CharField = models.CharField(
        max_length=100,
        unique=True,
        default="nickname",
        verbose_name="닉네임"
    )
    phone_number: models.CharField = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="전화번호"
    )
    is_staff: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="스태프 여부"
    )
    is_admin: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="관리자 여부"
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="활성화 여부"
    )
    last_login: Optional[models.DateTimeField] = models.DateTimeField(
        auto_now=True,
        null=True,
        verbose_name="마지막 로그인"
    )

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects: UserManager = UserManager()

    class Meta:
        verbose_name: str = "사용자"
        verbose_name_plural: str = "사용자들"

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm: str, obj: Optional[Any] = None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_admin

    @property
    def is_superuser(self) -> bool:
        return self.is_admin

    @staticmethod
    def activate_user(email: str) -> None:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserNotFoundError

        user.is_active = True
        user.save()


class Token:
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
    def generate_token(auth_user: User) -> "Token":
        refresh = RefreshToken.for_user(user=auth_user)
        return Token(
            access=str(refresh.access_token),
            refresh=str(refresh)
        )

    @staticmethod
    def refresh_token(refresh: str) -> "Token":
        # 내부적으로 TokenBackend를 거쳐 String -> Token으로 변환
        new_refresh = RefreshToken(refresh)
        return Token(
            access=str(new_refresh.access_token),
            refresh=str(new_refresh)
        )

    @staticmethod
    def revoke_token(refresh: str) -> None:
        old_token = RefreshToken(refresh)
        old_token.blacklist()
