from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponseNotFound

from apps.core.models import Profile


class UsersView(View):
    def get(self, request: HttpRequest):
        template_name = "dashboard/users.html"
        return render(request=request, template_name=template_name)


class UsersDetailsView(View):
    def get(self, request: HttpRequest, pk: int):
        profile_query = Profile.objects.filter(pk=pk)
        if not profile_query.exists():
            return HttpResponseNotFound()

        template_name = "dashboard/user_details.html"
        profile = profile_query.first()
        context = {"profile": profile}
        return render(
            request=request,
            template_name=template_name,
            context=context,
        )
