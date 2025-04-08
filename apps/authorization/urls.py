from django.urls import path
from apps.authorization.views import auth_views, provider_views, ad_connection_views

urlpatterns = [
    path(
        "login",
        auth_views.DefaultLogin.as_view(),
        name="default_login",
    ),
    path(
        "login/ad/<int:pk>",
        ad_connection_views.ADLogin.as_view(),
        name="ad_login",
    ),
    path(
        "login/activedirectory",
        auth_views.ActiveDirectorLogin.as_view(),
        name="ad_login",
    ),
    path(
        "providers",
        provider_views.ProviderList.as_view(),
        name="providers",
    ),
    # AD Connection
    path(
        "activedirectory/create",
        ad_connection_views.CreateADProvider.as_view(),
        name="ad_create",
    ),
    path(
        "activedirectory/<int:pk>/details",
        ad_connection_views.ADConnectionDetails.as_view(),
        name="ad_details",
    ),
    path(
        "activedirectory/<int:pk>/update",
        ad_connection_views.EditADProvider.as_view(),
        name="ad_edit",
    ),
    path(
        "activedirectory/create",
        ad_connection_views.CreateADProvider.as_view(),
        name="ad_create",
    ),
    path(
        "activedirectory/<int:pk>/details",
        ad_connection_views.ADConnectionDetails.as_view(),
        name="ad_details",
    ),
    path(
        "activedirectory",
        ad_connection_views.ADConnectionUsers.as_view(),
        name="active_directory",
    ),
]
