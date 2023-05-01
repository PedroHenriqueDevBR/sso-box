from django.urls import path
from apps.dashboard.views import dashboard_views, application_views

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
]
