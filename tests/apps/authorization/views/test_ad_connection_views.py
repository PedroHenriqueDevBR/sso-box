from django.test import TestCase, Client
from django.urls import reverse

from apps.authorization.models import ADConnection, Provider

from tests.utils.authorization_db import provider_fake, ad_connection_fake


class CreateADProviderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("ad_create")

    def test_should_return_ad_edit_templante(self):
        template_name = "auth/ad_connection/create_ad_connection.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)

    def test_should_return_bad_request_invalid_form(self):
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Invalid form data" in str(response.content))

    def test_should_return_bad_request_invalid_form_empty_data(self):
        data = {
            "name": "",
            "description": "",
            "address": "",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Invalid form data" in str(response.content))

    def test_should_invalid_request_server_already_exists(self):
        ADConnection.objects.create(address="128.0.0.1")
        data = {
            "name": "Main Server",
            "description": "Main Server",
            "address": "128.0.0.1",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Invalid form data" in str(response.content))

    def test_should_create_ad_connection_object(self):
        data = {
            "name": "Main Server",
            "description": "Main Server",
            "address": "128.0.0.2",
        }
        response = self.client.post(self.url, data=data)
        expected_url = reverse("ad_details", kwargs={"pk": 1})
        provider_count = Provider.objects.count()
        ad_connection_count = ADConnection.objects.count()
        self.assertRedirects(response, expected_url, status_code=302)
        self.assertEqual(provider_count, 1)
        self.assertEqual(ad_connection_count, 1)


class EditADProviderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("ad_edit", kwargs={"pk": 1})

    def test_should_redirect_connection_not_found(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_should_return_ad_edit_templante(self):
        template_name = "auth/ad_connection/create_ad_connection.html"
        ad_connection_fake()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)

    def test_should_return_bad_request_invalid_form(self):
        data = {}
        ad_connection_fake()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Invalid form data" in str(response.content))

    def test_should_return_bad_request_invalid_form_empty_data(self):
        data = {
            "name": "",
            "description": "",
            "address": "",
        }
        ad_connection_fake()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Invalid form data" in str(response.content))

    def test_should_update_ad_connection_object_with_provider(self):
        provider = provider_fake()
        ad_connection_fake(provider=provider)
        data = {
            "name": "Main Server",
            "description": "Main Server",
            "address": "128.0.0.222",
            "bind_dn": "username",
            "bind_password": "password",
        }

        response = self.client.post(self.url, data=data)
        ad_connection = ADConnection.objects.get(pk=1)
        provider = ad_connection.details
        expected_url = reverse("ad_details", kwargs={"pk": 1})

        self.assertRedirects(response, expected_url, status_code=302)
        self.assertEqual(ad_connection.address, "128.0.0.222")
        self.assertEqual(ad_connection.bind_dn, "username")
        self.assertEqual(ad_connection.bind_password, "password")
        self.assertEqual(provider.name, "Main Server")
        self.assertEqual(provider.description, "Main Server")

    def test_should_update_ad_connection_object_without_provider(self):
        ad_connection_fake()
        data = {
            "name": "Main Server",
            "description": "Main Server",
            "address": "128.0.0.222",
            "bind_dn": "username",
            "bind_password": "password",
        }

        response = self.client.post(self.url, data=data)
        ad_connection = ADConnection.objects.get(pk=1)
        provider = ad_connection.details
        provider_count = Provider.objects.count()
        expected_url = reverse("ad_details", kwargs={"pk": 1})

        self.assertRedirects(response, expected_url, status_code=302)
        self.assertEqual(ad_connection.address, "128.0.0.222")
        self.assertEqual(ad_connection.bind_dn, "username")
        self.assertEqual(ad_connection.bind_password, "password")
        self.assertIsNone(provider)
        self.assertEqual(provider_count, 0)


class ADConnectionDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("ad_details", kwargs={"pk": 1})

    def test_should_redirect_connection_not_found(self):
        response = self.client.get(self.url)
        expected_url = reverse("providers")
        self.assertRedirects(response, expected_url, status_code=302)

    def test_should_return_details_template(self):
        ad_connection_fake()
        template_name = "auth/ad_connection/details.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name)
