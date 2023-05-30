from apps.authorization.models import Provider, ADConnection


def provider_fake():
    return Provider.objects.create(
        name="",
        description="",
        is_active=True,
    )


def ad_connection_fake(provider=None):
    return ADConnection.objects.create(
        details=provider,
        address="128.0.0.1:123",
    )
