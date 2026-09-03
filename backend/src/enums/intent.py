from enum import StrEnum


class IntentMode(StrEnum):
    EXECUTE = "execute"
    CLARIFY = "clarify"
    OUT_OF_SCOPE = "out_of_scope"
