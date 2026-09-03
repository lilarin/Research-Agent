from enum import StrEnum


class IntentMode(StrEnum):
    EXECUTE = "execute"
    CLARIFY = "clarify"
    UNSUPPORTED = "unsupported"
