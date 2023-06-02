from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import View


class DefaultLogin(View):
    def get(self, request: HttpRequest):
        template_name = "auth/login.html"
        return render(request, template_name)


class ActiveDirectorLogin(View):
    def get(self, request: HttpRequest):
        template_name = "auth/login.html"
        return render(request, template_name)
