from django.contrib.auth.models import BaseUserManager
from typing import Any

from utils.validators import validate_super_user
from utils.common import assemble_kwargs, generate_id_by_login_type


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None,
                    login_type: str = "email", **extra_fields: Any):

        email = self.normalize_email(email)
        user_id = generate_id_by_login_type(login_type)
        total_fields = assemble_kwargs(
            id=user_id, email=email, login_type=login_type, **extra_fields
        )

        user = self.model(**total_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("login_type", "admin")

        validate_super_user(**extra_fields)

        user = self.create_user(email, password=password, **extra_fields)
        return user
