from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http.request import HttpRequest


class AuthenticatorService:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def authenticate_user(self, username: str) -> bool:
        User = get_user_model()
        users_query = User.objects.filter(username=username)

        if not users_query.exists():
            user = User.objects.create(first_name="first_name", username=username)
            login(request=self.request, user=user)
            return True

        user = users_query.first()
        if user is None:
            return False
        if not user.is_active:
            return False

        login(request=self.request, user=user)
        return True
