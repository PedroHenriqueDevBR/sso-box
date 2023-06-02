from django.contrib.auth import get_user_model
from django.test import TestCase

from tests.utils.core_db import user_type_fake, profile_fake


class UserTypeTestCase(TestCase):
    def test_instance_user_type(self):
        user_type = user_type_fake()
        self.assertEqual(user_type.name, "Administrator")


class ProfileTestCase(TestCase):
    def test_instance_without_references(self):
        profile = profile_fake()
        self.assertIsNone(profile.user)
        self.assertIsNone(profile.user_type)

    def test_instance_with_user_and_user_type(self):
        user_model = get_user_model()
        user = user_model.objects.create(username="", password="")
        user_type = user_type_fake()
        profile = profile_fake(
            user=user,
            user_type=user_type,
        )
        self.assertIsNotNone(profile.user)
        self.assertIsNotNone(profile.user_type)
