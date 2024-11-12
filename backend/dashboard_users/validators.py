import re
from typing import Any, Callable

from django.contrib.auth import validators as auth_validators
from django.core import validators as core_validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MyBaseValidator:
    def validate(self, field_value: Any) -> str | Callable:
        pass


class ASCIIUsernameValidator(MyBaseValidator, auth_validators.ASCIIUsernameValidator):
    regex = "^[\w.@_]+\Z"
    message = _(
        "Имя пользователя должно быть написано английскими буквами. Допускаются цифры и символы: [@_]"
        # "Test"
    )

    def validate(self, field_value: str) -> str | Callable:
        if not re.match(self.regex, field_value):
            return self.message

        return field_value


class FirstLastNameValidator(MyBaseValidator, auth_validators.UnicodeUsernameValidator):
    def __init__(self):
        super().__init__()

    regex = "^[A-ZА-Яa-zа-я]{1,64}$"
    message = _(
        "Фамилия/имя могут быть написаны только буквами!"
        # "TEST"
    )

    def validate(self, field_value: str) -> str | Callable:
        if not re.match(self.regex, field_value):
            return self.message

        return field_value


class EmailValidator(MyBaseValidator, core_validators.EmailValidator):
    message = _(
        "Введите правильный адрес электронной почты в формате [user@example.com] ."
        # "Enter the valid email [user@example.com] ."
    )

    def validate(self, field_value: str) -> str | Callable:
        try:
            self.__call__(field_value)
            return field_value
        except ValidationError:
            return self.message

