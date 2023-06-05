from typing import Optional
from django.http.request import QueryDict

from apps.authorization.models import ADConnection


def contains(info, data) -> bool:
    if info not in data:
        return False
    if len(data[info]) == 0:
        return False
    return True


def is_valid_ad_form(
    data: QueryDict,
    current_ad: Optional[ADConnection] = None,
) -> bool:
    if (
        not contains("name", data)
        or not contains("description", data)
        or not contains("address", data)
    ):
        return False
    if is_ad_connection_registered(data["address"], current_ad):
        return False
    return True


def is_ad_connection_registered(
    address: str,
    current_ad: Optional[ADConnection],
) -> bool:
    connections = ADConnection.objects.filter(address=address)
    if connections.exists():
        ad_connection = connections.first()
        if ad_connection is not None and current_ad is not None:
            if ad_connection.pk == current_ad.pk:
                return False
        return True
    return False
