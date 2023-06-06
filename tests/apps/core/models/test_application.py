from django.test import TestCase

from tests.utils.core_db import (
    application_fake,
    permission_fake,
    user_type_fake,
)


class UserTypeTestCase(TestCase):
    def test_instance_user_type(self):
        application = application_fake()
        self.assertIsNotNone(application.name)
        self.assertIsNotNone(application.desctiption)
        self.assertIsNotNone(application.url_feedback)
        self.assertIsNotNone(application.url_application)


class ApplicationPermissionsTestCase(TestCase):
    def test_instance_without_references(self):
        permissions = permission_fake()
        self.assertIsNone(permissions.application)
        self.assertIsNone(permissions.user_type)

    def test_instance_with_references(self):
        user_type = user_type_fake()
        application = application_fake()
        permission = permission_fake(
            user_type=user_type,
            application=application,
        )
        self.assertIsNotNone(permission.user_type)
        self.assertIsNotNone(permission.application)
