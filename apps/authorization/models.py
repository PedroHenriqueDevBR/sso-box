from django.db import models
from apps.core.models import Application, Profile


class Provider(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        ordering = ["name"]


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
    
    def __str__(self) -> str:
        application_name = ''
        profile_name = ''
        provider_name = ''
        
        if self.application is not None:
            application_name = self.application.name
        if self.profile is not None:
            application_name = self.profile.full_name
        if self.provider is not None:
            provider_name = self.provider.name
            
        return f'{provider_name} - {application_name} - {profile_name}'
    
    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connections"
        ordering = ["-created_at"]


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
    
    def __str__(self) -> str:
        return f"ADConnection to {self.address}"

    class Meta:
        verbose_name = "AD Connection"
        verbose_name_plural = "AD Connections"
        ordering = ["address"]
