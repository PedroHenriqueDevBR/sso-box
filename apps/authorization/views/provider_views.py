from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import View

from apps.authorization.models import Provider


class ProviderList(View):
    def get(self, request: HttpRequest):
        providers = Provider.objects.all()
        context = {"providers": providers}
        return render(
            request=request,
            template_name="auth/provider_list.html",
            context=context,
        )
