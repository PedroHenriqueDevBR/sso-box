from django.urls import path
from apps.authorization.views import auth_views, provider_views, ad_connection_views

urlpatterns = [
    path(
        "login",
        auth_views.DefaultLogin.as_view(),
        name="default_login",
    ),
    path(
        "providers",
        provider_views.ProviderList.as_view(),
        name="providers",
    ),
    # AD Connection
    path(
        "ad/create",
        ad_connection_views.CreateADProvider.as_view(),
        name="ad_create",
    ),
    path(
        "ad/details/<int:pk>",
        ad_connection_views.ADConnectionDetails.as_view(),
        name="ad_details",
    ),
]
