from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class MyASCIIUsernameValidator(ASCIIUsernameValidator):
    message = _(
        "Имя пользователя должно быть написано английскими буквами"
    )
