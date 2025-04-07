from django.contrib import admin
from apps.authorization.models import Provider, Connection, ADConnection


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "is_active")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "application",
        "profile",
        "provider",
        "token",
        "is_valid",
        "created_at",
    )
    search_fields = ("application__name", "profile__full_name", "provider__name")
    ordering = ("provider",)


@admin.register(ADConnection)
class ADConnectionAdmin(admin.ModelAdmin):
    list_display = ("id", "details", "address", "bind_dn", "ldap_base_dn")
    search_fields = ("details", "address")
