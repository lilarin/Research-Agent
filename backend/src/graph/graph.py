from langgraph.graph import END, START, StateGraph

from src.dataclasses.state import ExecutionState
from src.enums.nodes import GraphNode
from src.graph.nodes import ResearchGraphNodes


def build_research_graph(nodes: ResearchGraphNodes):
    builder = StateGraph(ExecutionState)

    builder.add_node(
        GraphNode.ROUTE,
        nodes.route,
        destinations=(
            GraphNode.CLARIFY.value,
            GraphNode.OUT_OF_SCOPE.value,
            GraphNode.SELECT_MODE.value,
        ),
    )
    builder.add_node(GraphNode.CLARIFY, nodes.clarify)
    builder.add_node(GraphNode.OUT_OF_SCOPE, nodes.out_of_scope)
    builder.add_node(
        GraphNode.SELECT_MODE,
        nodes.select_mode,
        destinations=(
            GraphNode.RETRIEVE_DOCUMENTS.value,
            GraphNode.RETRIEVE_WEB.value,
            GraphNode.RETRIEVE_DOCUMENTS_AND_WEB.value,
        ),
    )
    builder.add_node(GraphNode.RETRIEVE_DOCUMENTS, nodes.retrieve_documents)
    builder.add_node(GraphNode.RETRIEVE_WEB, nodes.retrieve_web)
    builder.add_node(
        GraphNode.RETRIEVE_DOCUMENTS_AND_WEB,
        nodes.retrieve_documents_and_web,
    )
    builder.add_node(GraphNode.ANSWER, nodes.answer)

    builder.add_edge(START, GraphNode.ROUTE)
    builder.add_edge(GraphNode.CLARIFY, END)
    builder.add_edge(GraphNode.OUT_OF_SCOPE, END)
    builder.add_edge(GraphNode.RETRIEVE_DOCUMENTS, GraphNode.ANSWER)
    builder.add_edge(GraphNode.RETRIEVE_WEB, GraphNode.ANSWER)
    builder.add_edge(
        GraphNode.RETRIEVE_DOCUMENTS_AND_WEB,
        GraphNode.ANSWER,
    )
    builder.add_edge(GraphNode.ANSWER, END)

    return builder.compile()
