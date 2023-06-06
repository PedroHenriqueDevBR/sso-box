from apps.core.models import (
    UserType,
    Profile,
    Application,
    ApplicationPermissions,
)


def user_type_fake() -> UserType:
    return UserType.objects.create(name="Administrator")


def profile_fake(user=None, user_type=None) -> Profile:
    return Profile.objects.create(
        user=user,
        user_type=user_type,
    )


def application_fake() -> Application:
    return Application.objects.create(
        name="",
        desctiption="",
        url_feedback="",
        url_application="",
    )


def permission_fake(
    application=None,
    user_type=None,
) -> ApplicationPermissions:
    return ApplicationPermissions.objects.create(
        application=application,
        user_type=user_type,
    )
