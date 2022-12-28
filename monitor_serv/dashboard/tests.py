import json
from pprint import pprint

from django.db.models import fields
from django.test import TestCase
from django import urls
from django import http
from . import models

# Create your tests here.


def add_targets():
    query = [
        models.Target(
            address="2.0.96.5", port=22, username="test", password="test", server_role=models.Target.ServerRole.MEDIA
        ),
        models.Target(
            address="2.0.96.6", port=22, username="test", password="test", server_role=models.Target.ServerRole.MEDIA
        ),
        models.Target(
            address="192.168.248.5", port=2250, username="info-admin", password="Rt3$YiOO",
            server_role=models.Target.ServerRole.HEAD
        ),
    ]

    for q in query:
        q.save()


def get_targets():
    return models.Target.objects.all()


class DashboardTests(TestCase):
    def test_index(self):
        response = self.client.get(urls.reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)

    def test_cpu_info(self):
        add_targets()
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:cpu_info"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_disk_info(self):
        add_targets()
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:disk_info"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, )

    def test_net_info(self):
        add_targets()
        response: http.JsonResponse = self.client.get(urls.reverse("dashboard:net_info"))
        print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, )

    def test_get_targets(self):
        objects = get_targets()
        print(objects)

    def test_add_objects(self):
        add_targets()
        objects = get_targets()
        print(objects)