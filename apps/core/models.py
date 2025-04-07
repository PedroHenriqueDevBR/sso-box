from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        verbose_name = "User Type"
        verbose_name_plural = "User Types"
        ordering = ["name"]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="profile",
        null=True,
        blank=True,
    )
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.SET_NULL,
        related_name="selected_profiles",
        null=True,
        blank=True,
    )
    
    @property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}" if self.user else '--'
    
    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Application(models.Model):
    name = models.CharField(max_length=150)
    desctiption = models.TextField(max_length=500)
    url_feedback = models.CharField(max_length=250)
    url_application = models.CharField(max_length=250)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ["name"]


class ApplicationPermissions(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        related_name="groups",
        null=True,
        blank=True,
    )
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.SET_NULL,
        related_name="selected_applications",
        null=True,
        blank=True,
    )
    
    def __str__(self) -> str:
        application_name = ''
        user_type_name = ''
        
        if self.application is not None:
            application_name = self.application.name
        if self.user_type is not None:
            user_type_name = self.user_type.name
        
        return f'{application_name} -> {user_type_name}'

    class Meta:
        verbose_name = "Application Permission"
        verbose_name_plural = "Application Permissions"
        ordering = ["application", "user_type"]
