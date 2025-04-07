from django.contrib import admin
from apps.core.models import UserType, Profile, Application, ApplicationPermissions


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "user_type", "full_name")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("user_type",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url_application", "url_feedback")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(ApplicationPermissions)
class ApplicationPermissionsAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "user_type")
    search_fields = ("application__name", "user_type__name")
    list_filter = ("application", "user_type")
