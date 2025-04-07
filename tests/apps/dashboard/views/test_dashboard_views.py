from django.test import TestCase, Client
from django.urls import reverse
from tests.utils.authenticator import AuthenticatorUtils


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.authenticator = AuthenticatorUtils(client=self.client)
        self.url = reverse("home")

    def test_should_redirect_to_login_page(self):
        response = self.client.get(self.url)
        url_esperada = reverse("default_login") + "?next=/"
        self.assertRedirects(response, url_esperada, status_code=302)

    def test_should_return_template(self):
        template_name = "dashboard/index.html"
        self.authenticator.autenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)
