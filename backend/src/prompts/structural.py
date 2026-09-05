from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.prompts.policies import SHARED_STRUCTURED_POLICIES

ROUTE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "\n\n".join(
                [
                    "Decide how to handle the user's request, taking the chat history into account.",
                    "Use execute when it is clear what the user wants to find out. "
                    "This includes finding, explaining, comparing, checking or summarizing "
                    "information. A question is enough; it does not need to be phrased as a command.",
                    "Use execute for any research, investigation, explanation, comparison, "
                    "fact-checking or summarization request, even when it is broad or "
                    "underspecified. Do not clarify only because the topic lacks constraints.",
                    "Use clarify only when the user provides a bare topic, keyword or "
                    "fragment with no question, goal or requested operation.",
                    "Use out_of_scope when the primary request is to write or generate "
                    "content, write code, perform an action, or provide dangerous, illegal "
                    "or non-research assistance. Factual explanations and research summaries "
                    "are within scope.",
                    "You are choosing the next step, not answering the question yet. "
                    "Missing document contents or search results are not a reason to "
                    "clarify an otherwise clear request; retrieval comes later.",
                    "Return JSON with a single field, mode: execute, clarify or out_of_scope.",
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
                    "Use documents only when the user clearly asks to search the provided documents. "
                    "Use web only when the user clearly asks for web or online information. "
                    "If neither source is specified or implied, use documents_and_web.",
                    "Write search_query as one concise, standalone search query. "
                    "Use relevant chat history to resolve references, keeping the user's "
                    "intent, key names and constraints such as dates or locations. "
                    "Remove conversational filler and answer-formatting requests. "
                    "Do not answer the question or add facts the user did not provide.",
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
