from enum import StrEnum


class GraphNode(StrEnum):
    ROUTE = "route"
    CLARIFY = "clarify"
    OUT_OF_SCOPE = "out_of_scope"
    RETRIEVE_DOCUMENTS = "retrieve_documents"
    RETRIEVE_WEB = "retrieve_web"
    RETRIEVE_DOCUMENTS_AND_WEB = "retrieve_documents_and_web"
    ANSWER = "answer"
