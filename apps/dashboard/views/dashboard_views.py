from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        user = request.user
        profile = None

        try:
            profile = user.profile  # type: ignore
        except AttributeError:
            pass

        if profile is not None:
            applications = profile.vinculed_applications()
            template_name = "dashboard/index.html"
            context = {"profile": profile, "applications": applications}
        else:
            template_name = "dashboard/no_profile_user.html"
            context = {}

        return render(
            request=request,
            template_name=template_name,
            context=context,
        )


class LogoutUser(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        logout(request=request)
        return redirect("home")
