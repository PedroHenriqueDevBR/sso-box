from django.views import View
from django.http.response import HttpResponseBadRequest
from django.http.request import HttpRequest, QueryDict
from django.shortcuts import redirect, render

from apps.authorization.models import Provider, ADConnection


class CreateADProvider(View):
    def get(self, request):
        template_name = "auth/ad_connection/create_ad_connection.html"
        return render(request, template_name)

    def post(self, request: HttpRequest):
        data = request.POST
        if not self.is_valid_form(data):
            return HttpResponseBadRequest("Invalid form data")

        name = data.get("name")
        description = data.get("description")
        is_active = data.get("is_active") or False
        provider = Provider.objects.create(
            name=name,
            description=description,
            is_active=is_active,
        )

        address = data.get("address")
        bind_dn = data.get("bind_dn")
        bind_password = data.get("bind_password")
        created_ad_connection = ADConnection.objects.create(
            details=provider,
            address=address,
            bind_dn=bind_dn,
            bind_password=bind_password,
        )
        return redirect("ad_details", created_ad_connection.pk)

    def is_valid_form(self, data: QueryDict):
        if (
            not self.contains("name", data)
            or not self.contains("description", data)
            or not self.contains("address", data)
        ):
            return False
        if self.is_provider_registered(data["address"]):
            return False
        return True

    def contains(self, info, data):
        if info not in data:
            return False
        if len(data[info]) == 0:
            return False
        return True

    def is_provider_registered(self, address: str):
        return ADConnection.objects.filter(address=address).exists()


class ADConnectionDetails(View):
    def get(self, request, pk):
        ad_connection_query = ADConnection.objects.filter(pk=pk)
        if not ad_connection_query.exists():
            return redirect("providers")

        template_name = "auth/ad_connection/details.html"
        ad_connection = ad_connection_query.first()
        context = {"ad_connection": ad_connection}
        return render(request, template_name, context)
