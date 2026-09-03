from pydantic import BaseModel

from src.enums.decisions import RouteMode, ContextMode


class RouteDecision(BaseModel):
    mode: RouteMode


class ModeDecision(BaseModel):
    mode: ContextMode
    search_query: str
