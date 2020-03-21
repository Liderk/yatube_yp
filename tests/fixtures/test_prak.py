from django.test import TestCase, Client
import datetime as dt



class PlansTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_access(self):
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 401)