from langgraph.types import Command

from src.enums.decisions import ContextMode, RouteMode
from src.enums.nodes import GraphNode
from src.schemas.decisions import ModeDecision, RouteDecision


class ResearchGraphTransitions:
    @staticmethod
    def route_start_command(
            *,
            decision: RouteDecision,
    ) -> Command[str]:
        if decision.mode is RouteMode.CLARIFY:
            destination = GraphNode.CLARIFY
        elif decision.mode is RouteMode.OUT_OF_SCOPE:
            destination = GraphNode.OUT_OF_SCOPE
        else:
            destination = GraphNode.SELECT_MODE

        return Command(goto=destination)

    @staticmethod
    def select_mode_command(
            *,
            decision: ModeDecision,
    ) -> Command[str]:
        if decision.mode is ContextMode.DOCUMENTS:
            destination = GraphNode.RETRIEVE_DOCUMENTS
        elif decision.mode is ContextMode.WEB:
            destination = GraphNode.RETRIEVE_WEB
        else:
            destination = GraphNode.RETRIEVE_DOCUMENTS_AND_WEB

        return Command(
            update={"search_query": decision.search_query},
            goto=destination,
        )
