from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    name = models.CharField(max_length=150)


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


class Application(models.Model):
    name = models.CharField(max_length=150)
    desctiption = models.TextField(max_length=500)
    url_feedback = models.CharField(max_length=250)
    url_application = models.CharField(max_length=250)


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
