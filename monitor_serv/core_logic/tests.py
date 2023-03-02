from django.test import TestCase

from dashboard.models import *


class TestChartCreator(TestCase):
    databases = {"iva_dashboard", "default"}
    fixtures = ["sc.json", "target", "cpu.json"]

    def setUp(self) -> None:
        self.cpu = CPU

    def test_create_chart_data(self):
        pass

        # builder.set_filter()
