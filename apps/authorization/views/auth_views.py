from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import View


class DefaultLogin(View):
    def get(self, request: HttpRequest):
        return render(request=request, template_name="auth/login.html")


class ActiveDirectorLogin(View):
    def get(self, request: HttpRequest):
        return render(request=request, template_name="auth/login.html")
