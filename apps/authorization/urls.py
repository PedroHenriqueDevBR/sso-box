from django.urls import path
from apps.authorization.views import auth_views, provider_views

urlpatterns = [
    path("login", auth_views.DefaultLogin.as_view(), name="default_login"),
    path("providers", provider_views.ProviderList.as_view(), name="providers"),
]
