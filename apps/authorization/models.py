from django.db import models
from apps.core.models import Application, Profile


class Provider(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)


class Connection(models.Model):
    token = models.CharField(max_length=150)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_created=True)
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        related_name="application_connections",
        null=True,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="profile_connections",
        null=True,
        blank=True,
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        related_name="provider_connections",
        null=True,
        blank=True,
    )


class ADConnection(models.Model):
    details = models.ForeignKey(
        Provider,
        related_name="ad_connections",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    bind_dn = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    bind_password = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
