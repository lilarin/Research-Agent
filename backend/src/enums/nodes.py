from enum import StrEnum


class GraphNode(StrEnum):
    ROUTE = "route"
    CLARIFY = "clarify"
    OUT_OF_SCOPE = "out_of_scope"
    SELECT_MODE = "select_mode"
    RETRIEVE_DOCUMENTS = "retrieve_documents"
    RETRIEVE_WEB = "retrieve_web"
    RETRIEVE_DOCUMENTS_AND_WEB = "retrieve_documents_and_web"
    ANSWER = "answer"

    @property
    def is_streamable(self) -> bool:
        return self in {
            self.ANSWER,
            self.CLARIFY,
            self.OUT_OF_SCOPE,
        }
