import ast
import json
import random
import unittest
from pprint import pprint

import core_logic.dbrouters
from django import http, urls
from django.test import TestCase
from django.test.runner import DiscoverRunner

from . import forms, models

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
            password="test"
        )
        target.save()
        pass


def add_targets():
    from core_logic import pass_handler
    from django.conf import settings

    key = settings.ENCRYPTION_KEY

    encrypted_passwd = pass_handler.encrypt_pass(password="test", encryption_key=key)

    query = [
        models.Target(
            id=17, address="192.168.248.5", port=9200, username="test", password=encrypted_passwd,
        ),
        models.Target(
            id=11, address="127.0.0.1", port=2000, username="test", password=encrypted_passwd,
        ),
        models.Target(
            id=12, address="127.0.0.1", port=2001, username="test", password=encrypted_passwd,
        ),
        models.Target(
            id=13, address="127.0.0.1", port=2002, username="test", password=encrypted_passwd,
        ),
        models.Target(
            id=18, address="192.168.248.5", port=9201, username="test", password=encrypted_passwd,
        ),
        models.Target(
            id=14, address="127.0.0.1", port=2003, username="test", password=encrypted_passwd,
        ),
    ]

    for q in query:
        q.save()


def add_settings():
    models.DashboardSettings(
        command_id=1,
        scraper_url="http://localhost:8001/api/monitor/metrics",
        scrape_interval=15
    ).save()


class DashboardTests(TestCase):
    databases = {'iva_dashboard', 'default'}


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

    def test_ram_info(self):
        add_targets()
        response = self.client.get(urls.reverse("dashboard:ram_info"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

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
        add_targets()
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:hostnamectl"))
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_net_model_filling(self):
        add_targets()
        res = self.client.get(urls.reverse("dashboard:net_info"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(isinstance(res.content, bytes), True)

    def test_disk_model_filling(self):
        add_settings()
        add_targets()
        res = self.client.get(urls.reverse("dashboard:disk_info"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(isinstance(res.content, bytes), True)

    def test_cpu_model_filling(self):
        add_settings()
        add_targets()
        res = self.client.get(urls.reverse("dashboard:cpu_top_info"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(isinstance(res.content, bytes), True)

    def test_ram_model_filling(self):
        add_settings()
        add_targets()
        res = self.client.get(urls.reverse("dashboard:ram_info"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(isinstance(res.content, bytes), True)

    def test_get_all_data_from_agent(self):
        add_targets()
        models.DashboardSettings(
            command_id=1,
            scraper_url="http://localhost:8001/api/monitor/metrics/targets/all",
            scraper_url_health_check="http://localhost:8001/api/monitor/ping",
            scrape_interval=15
        ).save()

        res = self.client.get(urls.reverse("dashboard:get_all_data_from_agent"))
        print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(isinstance(res.content, bytes), True)

    def test_check_agent_health(self):
        add_targets()
        models.DashboardSettings(
            command_id=1,
            scraper_url="http://localhost:8001/api/monitor/metrics/targets/all",
            scraper_url_health_check="http://localhost:8001/api/monitor/ping",
            scrape_interval=15
        ).save()

        res = self.client.get(urls.reverse("dashboard:check_agent_health"))
        print(res.content)
        self.assertEqual(res.status_code, 200)

