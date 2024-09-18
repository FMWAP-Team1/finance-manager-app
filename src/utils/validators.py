import re

from django.core.exceptions import ValidationError
from common.consts import LOGIN_TYPES

login_types = {login_type[0] for login_type in LOGIN_TYPES}


def validate_super_user(**extra_fields):
    if not (extra_fields.get('is_staff') is True and
            extra_fields.get('is_admin') is True and
            extra_fields.get('is_active') is True):
        raise ValidationError("입력된 슈퍼유저 정보가 유효하지 않습니다.")

    return True


def validate_create_user(email: str, password: str, login_type: str, **kwargs):
    validate_create_user_basic(email, login_type)
    validate_create_user_by_login_type(login_type, password)
    validate_create_user_extra_fields(**kwargs)


def validate_create_user_by_login_type(login_type, password):
    if login_type in ["email", "admin"]:
        validate_create_user_email(password)
    if login_type == "kakao":
        validate_create_user_kakao()


def validate_create_user_basic(email, login_type):
    validate_login_type(login_type)
    validate_email(email)


def validate_create_user_kakao():
    ...


def validate_create_user_email(password):
    validate_password(password)


def validate_kakao_id(kakao_id):
    if not kakao_id:
        raise ValueError("카카오 아이디는 필수입니다.")

    return kakao_id


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError("비밀번호에는 최소 하나의 영문자가 포함되어야 합니다.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.")
    if not re.search(r'[@$!%*#?&]', password):
        raise ValidationError("비밀번호에는 최소 하나의 특수문자(@$!%*#?&)가 포함되어야 합니다.")

    return password


def validate_phone_number(phone_number):
    if not re.match(r'^\d{3}-\d{3,4}-\d{4}$', phone_number):
        raise ValueError("올바른 전화번호 형식이 아닙니다. (예: 010-1234-5678)")

    return phone_number


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not email:
        raise ValueError("이메일 주소는 필수입니다.")

    if not re.match(email_regex, email):
        raise ValidationError("유효하지 않은 이메일 주소입니다.")

    return email


def validate_login_type(login_type):
    if login_type not in login_types:
        raise ValueError(f"로그인 타입은 [{str(login_types)}]중 하나 입니다.")

    return login_type


def validate_create_user_extra_fields(**extra_fields):
    if "phone_number" in extra_fields:
        validate_phone_number(extra_fields.get("phone_number"))
