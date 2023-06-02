from django.test import TestCase, Client
from django.urls import reverse


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("profile")

    def test_should_return_template(self):
        template_name = "dashboard/profile.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)
