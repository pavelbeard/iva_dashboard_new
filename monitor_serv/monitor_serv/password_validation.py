import re

from django.contrib.auth.password_validation import ValidationError
from django.utils.translation import gettext as _


class Validator:
    def validate(self, password, user=None):
        pass

    def get_help_text(self) -> _:
        pass


class SymbolsPasswordValidator(Validator):
    list_of_symbols = "`!@#$%^&*\_+~[]{}\\\';\":,.;?/"

    def validate(self, password, user=None):
        if not re.findall("`!@#\$%\^&\*\(\)_\+~\[\]\{\}\\\';\":,\.;\?/", password):
            raise ValidationError(
                _(f"The password must contain at least one symbol from this list: [ {self.list_of_symbols} ]")
            )

    def get_help_text(self) -> _:
        return _(f"Your password must contain at least one symbol from this list: [ {self.list_of_symbols} ]")


class UppercasePasswordValidator(Validator):
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _(f"The password must contain at least one symbol in uppercase, A-Z")
            )

    def get_help_text(self) -> _:
        return _("Your password must contain at least one symbol in uppercase, A-Z")


class NumberPasswordValidator(Validator):
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _(f"The password must contain at least one digit, 0-9")
            )

    def get_help_text(self) -> _:
        return _("Your password must contain at least one digit, 0-9")
