from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.prompts.policies import DOMAIN_POLICY, SECURITY_POLICY, STRUCTURE_POLICY

CLARIFICATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "\n\n".join(
                [
                    "Ask one concise clarification question for the research request.",
                    SECURITY_POLICY,
                    DOMAIN_POLICY,
                ]
            ),
        ),
        MessagesPlaceholder("chat_history", optional=True),
        (
            "human",
            "Question:\n{question}"
        ),
    ]
)

OUT_OF_SCOPE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "\n\n".join(
                [
                    "Briefly explain that the request is outside the supported research scope.",
                    SECURITY_POLICY,
                    DOMAIN_POLICY,
                ]
            ),
        ),
        (
            "human",
            "Question:\n{question}"
        ),
    ]
)

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "\n\n".join(
                [
                    "Answer the question using the provided context.",
                    SECURITY_POLICY,
                    DOMAIN_POLICY,
                    STRUCTURE_POLICY,
                ]
            ),
        ),
        MessagesPlaceholder("chat_history", optional=True),
        (
            "human",
            "Question:\n{question}\n\nContext:\n{context}",
        ),
    ]
)
