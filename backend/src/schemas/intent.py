from pydantic import BaseModel

from src.enums.intent import IntentMode
from src.enums.source import ExecutionSource


class IntentDecision(BaseModel):
    mode: IntentMode
    source: ExecutionSource | None = None
