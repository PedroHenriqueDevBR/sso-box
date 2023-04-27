from django.urls import path
from apps.dashboard.views import dashboard_views

urlpatterns = [
    path(
        "",
        dashboard_views.HomeView.as_view(),
        name="default_login",
    ),
]
