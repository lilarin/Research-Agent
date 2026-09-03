from enum import StrEnum


class RouteMode(StrEnum):
    EXECUTE = "execute"
    CLARIFY = "clarify"
    OUT_OF_SCOPE = "out_of_scope"


class ContextMode(StrEnum):
    DOCUMENTS = "documents"
    WEB = "web"
    DOCUMENTS_AND_WEB = "documents_and_web"
