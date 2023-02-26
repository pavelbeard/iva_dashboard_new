from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from . import forms, validators

# Create your tests here.

class TestAuth(TestCase):
    def setUp(self) -> None:
        self.username = "test230923"
        self.broken_username = "test-239203"
        self.first_name = "Pavel"
        self.broken_first_name = "pavel"
        self.last_name = "Borodin"
        self.broken_last_name = "borodin"
        self.password = "Rt3$YiOO"
        self.email = "test@gmail.com"
        self.broken_email = "test@.com"

    def test_login(self):
        client = self.client.username(username=self.username, password=self.password)
        self.assertEqual(client, True)

    def test_login_form(self):
        response = self.client.post(reverse("dashboard_users:login"), data={
            "username": self.username,
            "password": self.password
        })

        context_data = response.context['user']

        self.assertEqual(response.context['user'], AnonymousUser)

    def test_email_validator(self):
        email_validator = validators.EmailValidator()
        normal_result = email_validator.validate(self.email)
        broken_result = email_validator.validate(self.broken_email)

        self.assertEqual(self.email, normal_result)
        self.assertEqual(Exception, type(broken_result))

    def test_username_validator(self):
        username_validator = validators.ASCIIUsernameValidator()
        normal_result = username_validator.validate(self.username)
        broken_result = username_validator.validate(self.broken_username)

        self.assertEqual(self.username, normal_result)
        self.assertEqual(_("Test"), broken_result)

    def test_first_name_last_name(self):
        fnln_validator = validators.FirstLastNameValidator()
        normal_result = fnln_validator.validate(self.first_name)
        broken_result = fnln_validator.validate(self.broken_last_name)

        self.assertEqual(self.first_name, normal_result)
        self.assertEqual(_("TEST"), broken_result)

    def test_user_create_form_validation(self):
        broken_request = HttpRequest
        broken_request.POST = {
            "username": self.broken_username,
            "first_name": self.broken_first_name,
            "last_name": self.broken_last_name,
            "email": self.broken_email,
            "password1": self.password,
            "password2": "Rt3$"
        }

        form = forms.NewUserForm(broken_request.POST)

        self.assertEqual(form.is_valid(), True)

