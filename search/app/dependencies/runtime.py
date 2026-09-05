from typing import cast

from starlette.requests import Request

from app.dataclasses.runtime import Runtime


def get_runtime(request: Request) -> Runtime:
    return cast(Runtime, request.app.state.runtime)
