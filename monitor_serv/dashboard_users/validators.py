from django.contrib.auth import validators
from django.utils.translation import gettext_lazy as _


class ASCIIUsernameValidator(validators.ASCIIUsernameValidator):
    regex = "^[\w.@_]+\Z"
    message = _(
        "Имя пользователя должно быть написано английскими буквами. Допускаются цифры и символы: [@_]"
    )


class FirstLastNameValidator(validators.UnicodeUsernameValidator):
    regex = "^[A-ZА-Я][a-zа-я]{1,64}$"
    message = _(
        "Фамилия/имя могут быть написаны только с большой буквы!"
    )
