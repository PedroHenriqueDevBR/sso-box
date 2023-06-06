from django.test import TestCase, Client
from django.urls import reverse


class DefaultLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("default_login")

    def test_should_return_template(self):
        template_name = "auth/login.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)


class ActiveDirectorLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("ad_login")

    def test_should_return_template(self):
        template_name = "auth/login.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)
