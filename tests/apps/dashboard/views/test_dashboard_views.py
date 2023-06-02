from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    def test_should_return_template(self):
        template_name = "dashboard/index.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)
