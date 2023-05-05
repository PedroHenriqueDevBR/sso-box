from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest


class HomeView(View):
    def get(self, request: HttpRequest):
        template_name = "dashboard/index.html"
        return render(request=request, template_name=template_name)
