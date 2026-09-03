from enum import StrEnum


class ExecutionSource(StrEnum):
    DOCUMENTS = "documents"
    WEB = "web"
    DOCUMENTS_AND_WEB = "documents_and_web"
