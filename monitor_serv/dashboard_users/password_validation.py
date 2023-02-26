import os
import re

from dashboard_users import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import ValidationError
from django.utils.translation import gettext as _

SALT = os.getenv("SALT", "lKzLscyp8+/Ni?P8Bw@#*DD0")


class Validator:
    def validate(self, password, user=None):
        pass

    def get_help_text(self) -> _:
        pass


class SymbolsPasswordValidator(Validator):
    list_of_symbols = "`!@#$%^&*\_+~[]{}\\\';\":,.;?/"

    def validate(self, password, user=None):
        if not re.findall(r"[`!@#\$%\^&\*\(\)_\+~\[\]\{\}\\\';\":,\.;\?/]", password):
            raise ValidationError(
                _(f"Пароль должен содержать хотя бы один символ из этого списка: [ {self.list_of_symbols} ]"),
                code="password_no_symbol"
            )

    def get_help_text(self) -> _:
        return _(f"Ваш пароль должен содержать хотя бы один символ из этого списка: [ {self.list_of_symbols} ]")


class UppercasePasswordValidator(Validator):
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _(f"Пароль должен содержать хотя бы одну букву в верхнем регистре, A-Z"),
                code="password_no_uppercase"
            )

    def get_help_text(self) -> _:
        return _("Ваш пароль должен содержать хотя бы одну букву в верхнем регистре, A-Z")


class NumberPasswordValidator(Validator):
    def validate(self, password, user=None):
        if not re.findall("[0-9]", password):
            raise ValidationError(
                _(f"Пароль должен содержать хотя бы одну цифру, 0-9"),
                code="password_no_number"
            )

    def get_help_text(self) -> _:
        return _("Ваш пароль должен содержать хотя бы одну цифру, 0-9")


class RepeatedPasswordValidator(Validator):
    def __init__(self):
        self.saved_passwd = None
        self.hashed_passwd = None

    def passwords(self, user, password):
        self.hashed_passwd = make_password(password=password, salt=SALT)
        return models.StoredPassword.objects.filter(user=user, password=self.hashed_passwd).first()

    def validate(self, password, user=None):
        if user is None:
            return

        saved_passwd = self.passwords(user, password)

        if saved_passwd is None:
            raise ValidationError(
                _("The password can't be same the same as previously used passwords."),
                code="password_not_may_be_same"
            )

    def password_changed(self, password, user=None):
        if user is None:
            return None

        saved_passwd = self.passwords(user, password)

        if saved_passwd is None:
            saved_passwd = models.StoredPassword.objects.create(user=user, password=user)
            saved_passwd.save()

    def get_help_text(self) -> _:
        return _("Your password can't be same the same as previously used passwords.")
