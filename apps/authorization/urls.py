from django.urls import path
from apps.authorization.views import auth_views

urlpatterns = [
    path("login", auth_views.default_login, name="default_login"),
]
