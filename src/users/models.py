from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from typing import Optional, Dict, Any, List

class UserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Dict[str, Any]) -> 'User':
        if not email:
            raise ValueError("이메일 주소는 필수 입력 항목입니다.")
        email = self.normalize_email(email)
        if not extra_fields.get('nickname') or not extra_fields.get('name'):
            raise ValueError("닉네임과 이름은 필수 입력 사항입니다.")
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Dict[str, Any]) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError('스태프 권한을 가져야 합니다.')
        if extra_fields.get('is_admin') is not True:
            raise ValidationError('반드시 관리자 권한을 가져야 합니다.')
        if extra_fields.get('is_active') is not True:
            raise ValidationError('반드시 활성 상태여야 합니다.')

        if 'nickname' not in extra_fields or 'name' not in extra_fields or 'phone_number' not in extra_fields:
            raise ValidationError('닉네임, 이름, 전화번호는 필수 입력 사항입니다.')

        try:
            user: User = self.create_user(email, password, **extra_fields)
        except ValueError as e:
            raise ValidationError(str(e))

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email: models.EmailField = models.EmailField(unique=True)
    nickname: models.CharField = models.CharField(max_length=30, unique=True, default="nickname")
    name: models.CharField = models.CharField(max_length=50)
    phone_number: models.CharField = models.CharField(max_length=20, unique=True)
    last_login: models.DateTimeField = models.DateTimeField(auto_now=True, null=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_admin: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['nickname', 'name', 'phone_number']

    objects: UserManager = UserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm: str, obj: Optional[Any] = None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_admin

    @property
    def is_superuser(self) -> bool:
        return self.is_admin