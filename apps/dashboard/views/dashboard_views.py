from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        template_name = "dashboard/index.html"
        return render(request=request, template_name=template_name)
