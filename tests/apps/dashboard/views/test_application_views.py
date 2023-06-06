from django.test import TestCase, Client
from django.urls import reverse

from tests.utils.core_db import application_fake


class ApplicationListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("applications")

    def test_should_return_template(self):
        template_name = "dashboard/applications.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)


class ApplicationDetailsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("application_details", kwargs={"pk": 1})

    def test_should_return_not_found_error(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_should_return_template_with_application(self):
        template_name = "dashboard/application_details.html"
        application_fake()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)
