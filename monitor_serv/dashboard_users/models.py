from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import validators

# Create your models here.


ascii_validator = validators.ASCIIUsernameValidator()
first_last_name_validator = validators.FirstLastNameValidator()
email_validator = validators.EmailValidator()


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=32, unique=True,
        error_messages={
            "unique": _("Пользователь с данным именем уже существует."),
        },
        validators=[ascii_validator],
        verbose_name="Имя пользователя"
    )
    first_name = models.CharField(
        max_length=64,
        validators=[first_last_name_validator],
        error_messages={
            "required": _("Обязательное поле."),
        },
        verbose_name="Имя:")
    last_name = models.CharField(
        max_length=64,
        validators=[first_last_name_validator],
        error_messages={
            "required": _("Обязательное поле."),
        },
        verbose_name="Фамилия:"
    )
    email = models.EmailField(
        max_length=64,
        unique=True,
        validators=[email_validator],
        verbose_name="Email:",
    )
    password = models.CharField(
        max_length=255,
        verbose_name="Пароль:"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="ACTIVE", help_text=
        _("Является ли пользователь активным?")
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name="ROOT", help_text=
        _("Является ли пользователь администратором?")
    )
    is_staff = models.BooleanField(
        default=False, verbose_name='STAFF', help_text=
        _("Имеет ли право пользователь заходить в панель администратора?")
    )
    groups = models.ManyToManyField(Group, blank=True, verbose_name="Группы")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        app_label = "dashboard_users"
