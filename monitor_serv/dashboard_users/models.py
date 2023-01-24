from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from . import validators

# Create your models here.


ascii_validator = validators.ASCIIUsernameValidator()
first_last_name_validator = validators.FirstLastNameValidator()
email_validator = validators.EmailValidator()


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=32, unique=True,
        help_text=_("Обязательное и уникальное. Длина имени пользователя максимум 32 символа."
                    "Только буквы, цифры и символы: [@_]"),
        error_messages={
            "unique": _("Пользователь с данным именем уже существует."),
        },
        validators=[ascii_validator],
        verbose_name="Имя пользоветеля"
    )
    first_name = models.CharField(
        max_length=64,
        help_text=_("Обязательное. Длина имени максимум 64 символа."
                    "Только с большой буквы"),
        validators=[first_last_name_validator],
        error_messages={
            "required": _("Обязательное поле."),
        },
        verbose_name="Имя:")
    last_name = models.CharField(
        max_length=64,
        help_text=_("Обязательное. Длина фамилии максимум 64 символа."
                    "Только с большой буквы"),
        validators=[first_last_name_validator],
        error_messages={
            "required": _("Обязательное поле."),
        },
        verbose_name="Фамилия:"
    )
    email = models.EmailField(
        max_length=64,
        unique=True,
        help_text=_("Обязательное и уникальное. Длина почты максимум 64 символа."
                    "Формат: username@example.com"),
        validators=[email_validator],
        verbose_name="Email",
    )
    password = models.CharField(
        max_length=255,
        verbose_name="Пароль:"
    )
    is_active = models.BooleanField(
        default=False, verbose_name="ACTIVE", help_text=
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
