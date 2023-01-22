from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import fields


# Create your models here.


class CustomUser(AbstractUser):
    email = fields.EmailField(unique=True)
    password = models.CharField('Хэш пароля', max_length=255, editable=False)


class StoredPassword(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    password = models.CharField(
        'Хэш пароля',
        max_length=255,
        editable=False
    )
    date = models.DateTimeField(
        'Дата',
        auto_now_add=True,
        editable=False
    )
