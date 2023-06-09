from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import View
from apps.authorization.models import ADConnection


class DefaultLogin(View):
    def get(self, request: HttpRequest):
        template_name = "auth/login.html"
        context = {
            "ad_connections": self.all_ad_connections(),
        }
        return render(request, template_name, context)

    def all_ad_connections(self):
        connections = ADConnection.objects.exclude(details=None)
        return connections.filter(details__is_active=True)


class ActiveDirectorLogin(View):
    def get(self, request: HttpRequest):
        template_name = "auth/login.html"
        return render(request, template_name)
