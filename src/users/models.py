from users.managers import UserManager
from utils import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from typing import Optional, Dict, Any, List


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email: models.EmailField = models.EmailField(unique=True)
    password: models.CharField = models.CharField(max_length=100)
    name: models.CharField = models.CharField(max_length=100)
    nickname: models.CharField = models.CharField(max_length=100, unique=True, default="nickname")
    phone_number: models.CharField = models.CharField(max_length=20, unique=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)
    is_admin: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=True)
    last_login: models.DateTimeField = models.DateTimeField(auto_now=True, null=True)


    USERNAME_FIELD: str = 'email'
    # REQUIRED_FIELDS: List[str] = ['nickname', 'name', 'phone_number']

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