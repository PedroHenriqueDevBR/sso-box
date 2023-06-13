from django.test.client import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class AuthenticatorUtils:
    def __init__(self, client: Client) -> None:
        self.client = client
        self.user = None

    def autenticate(self):
        self.client.logout()
        User = get_user_model()
        self.user = User(username="something")
        self.user.set_password("pass@123")
        self.user.save()
        self.client.login(
            username="something",
            password="pass@123",
        )

    def search_group(self, group_name):
        groups = Group.objects.filter(name=group_name)
        if groups.exists():
            return groups.first()
        return Group.objects.create(name=group_name)

    def turn_administrator(self):
        if self.user is None:
            return
        self.user.is_superuser = True
