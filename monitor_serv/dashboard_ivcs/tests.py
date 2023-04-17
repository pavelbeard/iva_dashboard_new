from django import urls
from django.test import TestCase

# Create your tests here.


class IvcsTests(TestCase):
    def test_get_data_from_access_log_record(self):
        res = self.client.get(urls.reverse("dashboard_ivcs:access_log_records"))
        print(res.content)
        self.assertEqual(res.status_code, 200)
