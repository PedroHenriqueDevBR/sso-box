from django.urls import path
from apps.dashboard.views import (
    dashboard_views,
    application_views,
    profile_views,
    users_views,
)

urlpatterns = [
    path(
        "",
        dashboard_views.HomeView.as_view(),
        name="home",
    ),
    path(
        "applications",
        application_views.ApplicationListView.as_view(),
        name="applications",
    ),
    path(
        "applications/<int:pk>",
        application_views.ApplicationDetailsView.as_view(),
        name="application_details",
    ),
    path(
        "profile",
        profile_views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "users",
        users_views.UsersView.as_view(),
        name="users",
    ),
]
