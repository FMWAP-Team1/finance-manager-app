from django.db import models
from django.utils import timezone
from datetime import datetime

class BaseModel(models.Model):
    created_dt: datetime = models.DateTimeField(
        verbose_name='생성일시',
        auto_now_add=True
    )
    updated_dt: datetime = models.DateTimeField(
        verbose_name='갱신일시',
        auto_now=True
    )

    class Meta:
        abstract = True
