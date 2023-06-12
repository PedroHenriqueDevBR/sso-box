from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        template_name = "dashboard/index.html"
        return render(request=request, template_name=template_name)


class LogoutUser(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        logout(request=request)
        return redirect("login")
