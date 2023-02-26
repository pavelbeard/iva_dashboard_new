from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class DashboardDetailTestCase(TestCase):
    def test_chartjs_cpu_view(self):
        res = self.client.get(reverse("dashboard_detail:cpu"))
        self.assertEqual(res.status_code, 200)