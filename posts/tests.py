# from django.test import TestCase
#
#
# # Create your tests here.
#
# class TestStringMethods(TestCase):
#     def test_length(self):
#         self.assertEqual(len("yatube"), 6)
#
#     def test_show_msg(self):
#         # действительно ли первый аргумент — True?
#         self.assertTrue(False, msg="Важная проверка на истинность")
from django.test import TestCase, Client
import datetime as dt


class PlansTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_access(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 302)

    def test_context_plans(self):
        response = self.client.get('')
        self.assertIn('posts', response.context)

    def test_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'index.html')
