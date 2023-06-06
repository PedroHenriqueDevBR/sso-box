from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import View

from apps.authorization.models import ADConnection, Provider
from apps.authorization.utils.formater import format_is_active_attribute
from apps.authorization.utils.validator import is_valid_ad_form


class CreateADProvider(View):
    def get(self, request: HttpRequest):
        template_name = "auth/ad_connection/create_ad_connection.html"
        return render(request, template_name)

    def post(self, request: HttpRequest):
        data = request.POST
        if not is_valid_ad_form(data=data):
            return HttpResponseBadRequest("Invalid form data")

        name = data.get("name")
        description = data.get("description")
        is_active = data.get("is_active")
        is_active = format_is_active_attribute(is_active)

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


class EditADProvider(View):
    def get(self, request: HttpRequest, pk: int):
        ad_connections_query = ADConnection.objects.filter(pk=pk)
        if not ad_connections_query.exists():
            return HttpResponseNotFound("Active Diretory provider not found!")

        ad_connection = ad_connections_query.first()
        template_name = "auth/ad_connection/create_ad_connection.html"
        context = {"ad_connection": ad_connection}
        return render(request, template_name, context=context)

    def post(self, request: HttpRequest, pk: int):
        ad_connections_query = ADConnection.objects.filter(pk=pk)
        if not ad_connections_query.exists():
            return HttpResponseNotFound("Active Diretory provider not found!")

        data = request.POST
        ad_connection = ad_connections_query.first()
        if ad_connection is not None:
            if not is_valid_ad_form(data, current_ad=ad_connection):
                return HttpResponseBadRequest("Invalid form data")

            self.update_ad_data(ad_connection=ad_connection, data=data)
            return redirect("ad_details", ad_connection.pk)
        return redirect("providers")

    def update_ad_data(self, ad_connection: ADConnection, data):
        address = data.get("address")
        bind_dn = data.get("bind_dn")
        bind_password = data.get("bind_password")
        updated_data = False

        if address is not None and address != ad_connection.address:
            ad_connection.address = address
            updated_data = True
        if bind_dn is not None and bind_dn != ad_connection.bind_dn:
            ad_connection.bind_dn = bind_dn
            updated_data = True
        if bind_password is not None and bind_password != ad_connection.bind_password:
            ad_connection.bind_password = bind_password
            updated_data = True
        if updated_data:
            ad_connection.save()

        if ad_connection.details is not None:
            self.update_provider_details(provider=ad_connection.details, data=data)

    def update_provider_details(self, provider: Provider, data):
        name = data.get("name")
        description = data.get("description")
        is_active = data.get("is_active")
        is_active = format_is_active_attribute(is_active)
        updated_provider = False

        if name is not None and name != provider.name:
            provider.name = name
            updated_provider = True
        if description is not None and description != provider.description:
            provider.description = description
            updated_provider = True
        provider.is_active = is_active
        if updated_provider:
            provider.save()


class ADConnectionDetails(View):
    def get(self, request: HttpRequest, pk: int):
        ad_connection_query = ADConnection.objects.filter(pk=pk)
        if not ad_connection_query.exists():
            return redirect("providers")

        template_name = "auth/ad_connection/details.html"
        ad_connection = ad_connection_query.first()
        context = {"ad_connection": ad_connection}
        return render(request, template_name, context)
