from apps.authorization.models import Provider, ADConnection


def provider_fake() -> Provider:
    return Provider.objects.create(
        name="Test",
        description="Test description",
        is_active=True,
    )


def ad_connection_fake(provider=None) -> ADConnection:
    return ADConnection.objects.create(
        details=provider,
        address="128.0.0.1:123",
    )
