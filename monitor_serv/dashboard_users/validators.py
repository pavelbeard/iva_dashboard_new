from django.contrib.auth import validators as auth_validators
from django.core import validators as core_validators
from django.utils.translation import gettext_lazy as _


class ASCIIUsernameValidator(auth_validators.ASCIIUsernameValidator):
    regex = "^[\w.@_]+\Z"
    message = _(
        "Имя пользователя должно быть написано английскими буквами. Допускаются цифры и символы: [@_]"
    )


class FirstLastNameValidator(auth_validators.UnicodeUsernameValidator):
    regex = "^[A-ZА-Я][a-zа-я]{1,64}$"
    message = _(
        "Фамилия/имя могут быть написаны только с большой буквы!"
    )


class EmailValidator(core_validators.EmailValidator):
    message = _(
        "Введите правильный адрес электронной почты в формате [user@example.com] ."
    )
