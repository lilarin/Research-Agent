from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.prompts.policies import SHARED_STRUCTURED_POLICIES

ROUTE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "\n\n".join(
                [
                    "Classify the research request.",
                    "Return JSON with exactly one field: mode.",
                    "mode must be one of: execute, clarify, out_of_scope.",
                    *SHARED_STRUCTURED_POLICIES,
                ]
            ),
        ),
        MessagesPlaceholder("chat_history", optional=True),
        (
            "human",
            "Latest question:\n{question}"
        ),
    ]
)

MODE_SELECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "\n\n".join(
                [
                    "Select the context source for the research request.",
                    "Return JSON with exactly two fields: mode and search_query.",
                    "mode must be one of: documents, web, documents_and_web.",
                    "search_query must be a concise query derived from the question.",
                    *SHARED_STRUCTURED_POLICIES,
                ]
            ),
        ),
        MessagesPlaceholder("chat_history", optional=True),
        (
            "human",
            "Latest question:\n{question}"
        ),
    ]
)
