from pydantic import BaseModel

from src.enums.decisions import ContextMode, RouteMode


class RouteDecision(BaseModel):
    mode: RouteMode


class ModeDecision(BaseModel):
    mode: ContextMode
    search_query: str
