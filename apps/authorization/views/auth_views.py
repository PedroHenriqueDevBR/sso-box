from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http.request import QueryDict
from django.views.generic import View
from apps.authorization.models import ADConnection
from django.contrib import messages
from django.contrib.auth import authenticate, login


class DefaultLogin(View):
    def get(self, request: HttpRequest):
        template_name = "auth/login.html"
        context = {
            "ad_connections": self.all_ad_connections(),
        }
        return render(request, template_name, context)

    def post(self, request: HttpRequest):
        data = request.POST
        if not self.is_valid_data(request=request, data=data):
            return redirect("default_login")

        if self.valid_authenticate(request=request, data=data):
            return redirect("home")

        messages.add_message(request, messages.ERROR, "Invalid credentials!")
        return redirect("default_login")

    def valid_authenticate(self, request, data):
        username = data.get("username") or ""
        password = data.get("password") or ""
        user = authenticate(username=username, password=password)
        if user is None:
            return False

        login(request, user=user)
        return True

    def is_valid_data(self, request: HttpRequest, data: QueryDict) -> bool:
        username = data.get("username") or ""
        password = data.get("password") or ""
        is_valid = True

        if len(username) == 0:
            messages.add_message(
                request,
                messages.WARNING,
                "Username is required",
            )

        if len(password) == 0:
            messages.add_message(
                request,
                messages.WARNING,
                "Password is required",
            )

        return is_valid

    def all_ad_connections(self):
        connections = ADConnection.objects.exclude(details=None)
        return connections.filter(details__is_active=True)


class ActiveDirectorLogin(View):
    def get(self, request: HttpRequest):
        template_name = "auth/login.html"
        return render(request, template_name)
