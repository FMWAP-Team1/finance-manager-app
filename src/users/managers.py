from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from typing import Optional, Dict, Any, List

class UserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Dict[str, Any]) -> 'User':
        if not email:
            raise ValueError("이메일 주소는 필수 입력 항목입니다.")
        email = self.normalize_email(email)
        if not extra_fields.get('name') or not extra_fields.get('phone_number'):
            raise ValueError("이름과 전화번호는 필수 입력 사항입니다.")
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