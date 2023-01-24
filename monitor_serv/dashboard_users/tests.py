from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class TestLogin(TestCase):
    def setUp(self) -> None:
        self.login = "test230923"
        self.password = "Rt3$YiOO"

    def test_login(self):
        client = self.client.login(username=self.login, password=self.password)
        self.assertEqual(client, True)

    def test_login_form(self):
        response = self.client.post(reverse("dashboard_users:login"), data={
            "username": self.login,
            "password": self.password
        })

        context_data = response.context['user']

        self.assertEqual(response.context['user'].is_active, False)


