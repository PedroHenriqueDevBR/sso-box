from django.urls import path
from apps.authorization.views import auth_views

urlpatterns = [
    path("login", auth_views.DefaultLogin.as_view(), name="default_login"),
]
