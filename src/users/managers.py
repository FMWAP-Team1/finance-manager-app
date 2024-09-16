from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from typing import Dict, Any
import re

class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, name: str, phone_number: str, **extra_fields: Dict[str, Any]) -> 'User':
        if not self._is_valid_user(email=email, password=password, name=name, phone_number=phone_number):
            raise ValidationError("입력된 사용자 정보가 유효하지 않습니다.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, name: str, phone_number: str, nickname: str, **extra_fields: Dict[str, Any]) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['nickname'] = nickname

        if not self._is_valid_superuser(extra_fields):
            raise ValidationError("입력된 슈퍼유저 정보가 유효하지 않습니다.")

        try:
            user = self.create_user(email, password, name, phone_number, **extra_fields)
        except ValidationError as e:
            raise ValidationError(str(e))

        return user

    def _is_valid_user(self, email: str, password: str, name: str, phone_number: str) -> bool:
        try:
            self._validate_email(email)
            self._validate_password(password)
            self._validate_name(name)
            self._validate_phone_number(phone_number)
            return True
        except ValueError:
            return False

    def _is_valid_superuser(self, extra_fields: Dict[str, Any]) -> bool:
        return (
            extra_fields.get('is_staff') is True and
            extra_fields.get('is_admin') is True and
            extra_fields.get('is_active') is True and
            'nickname' in extra_fields
        )

    def _validate_email(self, email: str) -> None:
        if not email:
            raise ValueError("이메일 주소는 필수 입력 항목입니다.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("유효한 이메일 주소를 입력해주세요.")

    def _validate_password(self, password: str) -> None:
        if not password:
            raise ValueError("비밀번호는 필수 입력 항목입니다.")
        if len(password) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다.")

    def _validate_name(self, name: str) -> None:
        if not name:
            raise ValueError("이름은 필수 입력 항목입니다.")

    def _validate_phone_number(self, phone_number: str) -> None:
        if not phone_number:
            raise ValueError("전화번호는 필수 입력 항목입니다.")
        if not re.match(r'^\d{3}-\d{3,4}-\d{4}$', phone_number):
            raise ValueError("올바른 전화번호 형식이 아닙니다. (예: 010-1234-5678)")