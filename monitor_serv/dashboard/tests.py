import json
import random
import unittest
from pprint import pprint

from django import http
from django import urls
from django.test import TestCase
from django.test.runner import DiscoverRunner

from . import forms
from . import models


# Create your tests here.


class EmojiTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emojis = self.dots
        self.dots = False

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        super().addSuccess(test)
        if self.emojis:
            self.stream.write('✅')
            self.stream.flush()

    def addError(self, test: unittest.case.TestCase, err) -> None:
        super().addError(test, err)
        if self.emojis:
            self.stream.write('😵')
            self.stream.flush()

    def addFailure(self, test: unittest.case.TestCase, err) -> None:
        super().addFailure(test, err)
        if self.emojis:
            self.stream.write('❌')
            self.stream.flush()

    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        if self.emojis:
            self.stream.write('⏭️')
            self.stream.flush()

    def addExpectedFailure(self, test: unittest.case.TestCase, err) -> None:
        super().addExpectedFailure(test, err)
        if self.emojis:
            self.stream.write('❎')
            self.stream.flush()

    def addUnexpectedSuccess(self, test: unittest.case.TestCase) -> None:
        super().addUnexpectedSuccess(test)
        if self.emojis:
            self.stream.write('😳')
            self.stream.flush()

    def printErrors(self) -> None:
        if self.emojis:
            self.stream.writeln()
        super().printErrors()


class EmojiTestRunner(DiscoverRunner):
    def get_resultclass(self):
        klass = super().get_resultclass()
        if klass is None:
            return EmojiTestResult

        return klass


class TestAuth(TestCase):
    def setUp(self) -> None:
        self.randomint = random.randint(0, 100)
        self.request = http.HttpRequest()
        self.user_data = {
            "username": f"test{self.randomint}",
            "first_name": f"test{self.randomint}",
            "last_name": f"test{self.randomint}",
            "email": f"test{self.randomint}@gmail.com",
            "password1": f"Rt3%{self.randomint}AA",
            "password2": f"RT3%{self.randomint}AA",
        }

    def test_signup(self):
        self.request.POST = {
            "username": f"test{self.randomint}",
            "first_name": f"test{self.randomint}",
            "last_name": f"test{self.randomint}",
            "email": f"test{self.randomint}@gmail.com",
            "password1": f"Rt3%{self.randomint}AA",
            "password2": f"RT3%{self.randomint}AA",
        }

        form = forms.SignupForm(self.request.POST)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        pass
        # self.assertEqual()

    def test_user_create(self):
        del self.user_data['password1']
        self.user_data['password'] = self.user_data.pop('password2')

        user = models.CustomUser.objects.create_user(**self.user_data)
        user.save()
        pass

    def test_target_create(self):
        target = models.Target.objects.create(
            address="90.50.0.1",
            port=22,
            username="test",
            password="test",
            server_role=models.Target.ServerRole.MEDIA)
        target.save()
        pass


def add_targets():
    from logic import pass_handler
    from django.conf import settings

    key = settings.ENCRYPTION_KEY

    encrypted_passwd = pass_handler.encrypt_pass(password="test", encryption_key=key)

    query = [
        models.Target(
            address="2.0.96.5", port=22, username="test", password=encrypted_passwd,
            server_role=models.Target.ServerRole.MEDIA
        ),
        models.Target(
            address="2.0.96.6", port=22, username="test", password=encrypted_passwd,
            server_role=models.Target.ServerRole.MEDIA
        ),
        # models.Target(
        #     address="192.168.248.4", port=2249, username="info-admin", password="Rt3$YiOO",
        #     server_role=models.Target.ServerRole.HEAD
        # ),
    ]

    for q in query:
        q.save()


class DashboardTests(TestCase):
    @classmethod
    def add_targets(cls):
        from logic import pass_handler
        from django.conf import settings

        key = settings.ENCRYPTION_KEY

        encrypted_passwd = pass_handler.encrypt_pass(password="test", encryption_key=key)

        query = [
            models.Target(
                address="2.0.96.5", port=22, username="test", password=encrypted_passwd,
                server_role=models.Target.ServerRole.MEDIA
            ),
            models.Target(
                address="2.0.96.6", port=22, username="test", password=encrypted_passwd,
                server_role=models.Target.ServerRole.MEDIA
            ),
            # models.Target(
            #     address="192.168.248.4", port=2249, username="info-admin", password="Rt3$YiOO",
            #     server_role=models.Target.ServerRole.HEAD
            # ),
        ]

        for q in query:
            q.save()

    @classmethod
    def get_targets(cls):
        return models.Target.objects.all()

    def setUp(self) -> None:
        # self.add_targets()
        # self.targets = self.get_targets()
        self.targets = None

    def test_index(self):
        response = self.client.get(urls.reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_cpu_info(self):
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:cpu_info"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_cpu_top_info(self):
        add_targets()
        response = self.client.get(urls.reverse("dashboard:cpu_top_info"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_disk_info(self):
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:disk_info"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, )

    def test_net_info(self):
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:net_info"))
        print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, )

    def test_get_targets(self):
        objects = self.targets
        print(objects)

    def test_add_objects(self):
        objects = self.targets
        print(objects)

    def test_db_filling(self):
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:dal_hostnamectl"))
        print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
