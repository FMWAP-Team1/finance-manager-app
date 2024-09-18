from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from typing import Optional, Any, List

from users.managers import UserManager
from users.exceptions import UserNotFoundError
from common.models import BaseModel
from common.consts import LOGIN_TYPES


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.CharField(max_length=128, primary_key=True, verbose_name="고유ID")
    email = models.EmailField(unique=True, verbose_name="이메일")
    password = models.CharField(max_length=128, null=True, verbose_name="비밀번호")
    name = models.CharField(max_length=100, null=True, verbose_name="이름")
    nickname = models.CharField(max_length=100, null=True, verbose_name="닉네임")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="전화번호")
    is_staff = models.BooleanField(default=False, verbose_name="스태프 여부")
    is_admin = models.BooleanField(default=False, verbose_name="관리자 여부")
    is_active = models.BooleanField(default=False, verbose_name="활성화 여부")
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="마지막 로그인")
    login_type = models.CharField(max_length=15, choices=LOGIN_TYPES, verbose_name="로그인 타입")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    class Meta:
        verbose_name: str = "사용자"
        verbose_name_plural: str = "사용자들"

    def __str__(self) -> str:
        return str(self.email)

    def has_perm(self, perm: str, obj: Optional[Any] = None) -> bool:
        return bool(self.is_admin)

    def has_module_perms(self, app_label: str) -> bool:
        return bool(self.is_admin)

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
