from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponseNotFound

from apps.core.models import Application


class ApplicationListView(View):
    def get(self, request: HttpRequest):
        template_name = "dashboard/applications.html"
        return render(request=request, template_name=template_name)


class ApplicationDetailsView(View):
    def get(self, request: HttpRequest, pk: int):
        applications_query = Application.objects.filter(pk=pk)
        if not applications_query.exists():
            return HttpResponseNotFound()

        template_name = "dashboard/application_details.html"
        application = applications_query.first()
        context = {"application": application}
        return render(
            request=request,
            template_name=template_name,
            context=context,
        )
