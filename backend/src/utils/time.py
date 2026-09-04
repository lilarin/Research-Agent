from datetime import datetime


def current_datetime() -> str:
    now = datetime.now().astimezone()
    hour = now.strftime("%I").lstrip("0") or "12"
    timezone = now.tzname() or "UTC"
    return (
        f"{now:%A, %B} {now.day}, {now:%Y} at {hour}:{now:%M} {now:%p} {timezone}"
    )
