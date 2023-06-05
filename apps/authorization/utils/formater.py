def format_is_active_attribute(is_active) -> bool:
    if is_active is None:
        return False
    elif is_active == "on":
        return True
    return False
