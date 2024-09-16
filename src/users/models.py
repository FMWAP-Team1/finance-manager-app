from django.db import models
from users.managers import UserManager
from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from typing import Optional, Any, List

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