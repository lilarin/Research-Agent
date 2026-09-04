from datetime import datetime


def current_datetime() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
