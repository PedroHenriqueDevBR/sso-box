from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest


class ApplicationListView(View):
    def get(self, request: HttpRequest):
        template_name = "dashboard/applications.html"
        return render(request=request, template_name=template_name)


class ApplicationDetailsView(View):
    def get(self, request: HttpRequest, pk: int):
        template_name = "dashboard/application_details.html"
        context = {"pk": pk}
        return render(
            request=request,
            template_name=template_name,
            context=context,
        )
