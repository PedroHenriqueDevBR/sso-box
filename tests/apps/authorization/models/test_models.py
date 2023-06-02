from django.test import TestCase
from apps.authorization.models import ADConnection, Provider


class ADConnectionTestCase(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_instance_ad_connection_without_provider_details(self):
        ad_connection = ADConnection.objects.create(address='ldap://127.0.0.1')
        self.assertIsNone(ad_connection.bind_dn)
        self.assertIsNone(ad_connection.bind_password)

    def test_instance_ad_connection_full_data(self):
        details = Provider.objects.create(
            name='',
            description='',
            is_active=True,
        )
        ad_connection = ADConnection.objects.create(
            details=details,
            address='ldap://127.0.0.1',
            bind_dn='',
            bind_password='',
        )
        self.assertIsNotNone(ad_connection.bind_dn)
        self.assertIsNotNone(ad_connection.bind_password)
