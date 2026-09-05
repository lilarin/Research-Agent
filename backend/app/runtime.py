from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from httpx import AsyncClient
from langchain_litellm import ChatLiteLLMRouter
from litellm.router import Router
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

from app.config import Settings
from app.database import close_database, init_database
from app.dataclasses.runtime import Runtime
from src.graph.graph import build_research_graph
from src.graph.nodes import ResearchGraphNodes
from src.integrations.documents import DocumentsClient
from src.integrations.search import SearchClient
from src.repositories.chat import ChatHistoryRepository
from src.services.chat import ChatService
from src.services.documents_context import DocumentsContextService
from src.services.web_context import WebContextService
from src.steps.answer import AnswerStep
from src.steps.clarification import ClarificationStep
from src.steps.mode_selection import ModeSelectionStep
from src.steps.out_of_scope import OutOfScopeStep
from src.steps.routing import RoutingStep


def build_chat_service(
        settings: Settings,
        *,
        search: SearchClient,
        documents: DocumentsClient,
) -> ChatService:
    router = Router(
        model_list=[
            {
                "model_name": settings.llm_model,
                "litellm_params": {
                    "model": f"ollama_chat/{settings.llm_model}",
                    "api_base": settings.model_base_url,
                    "think": settings.llm_answer_think,
                },
            },
        ],
        num_retries=settings.llm_max_retries,
        retry_after=settings.llm_retry_after,
        timeout=settings.llm_timeout,
    )
    structured_router = Router(
        model_list=[
            {
                "model_name": settings.llm_model,
                "litellm_params": {
                    "model": f"ollama_chat/{settings.llm_model}",
                    "api_base": settings.model_base_url,
                    "think": False,
                },
            },
        ],
        num_retries=settings.llm_max_retries,
        retry_after=settings.llm_retry_after,
        timeout=settings.llm_timeout,
    )
    model = ChatLiteLLMRouter(
        router=router,
        model_name=settings.llm_model,
        streaming=True,
    )
    structured_model = ChatLiteLLMRouter(
        router=structured_router,
        model_name=settings.llm_model,
        streaming=True,
    )
    nodes = ResearchGraphNodes(
        routing_step=RoutingStep(model=structured_model),
        mode_selection_step=ModeSelectionStep(model=structured_model),
        clarification_step=ClarificationStep(model=model),
        out_of_scope_step=OutOfScopeStep(model=model),
        answer_step=AnswerStep(model=model),
        documents_context=DocumentsContextService(
            documents=documents,
            max_search=settings.documents_max_search,
            max_retrieval=settings.documents_max_retrieval,
        ),
        web_context=WebContextService(
            search=search,
            max_sources=settings.search_max_sources,
        ),
    )
    return ChatService(
        graph=build_research_graph(nodes),
        history=ChatHistoryRepository(
            messages_limit=settings.chat_history_messages_limit,
        ),
    )


@asynccontextmanager
async def open_runtime(settings: Settings) -> AsyncIterator[Runtime]:
    tracer_provider = register(
        project_name=settings.phoenix_project_name,
        endpoint=settings.phoenix_collector_endpoint,
    )
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

    async with AsyncExitStack() as stack:
        await init_database(settings)
        stack.push_async_callback(close_database)

        search_http = await stack.enter_async_context(
            AsyncClient(
                base_url=settings.search_base_url,
                timeout=settings.http_timeout,
            )
        )
        documents_http = await stack.enter_async_context(
            AsyncClient(
                base_url=settings.documents_base_url,
                timeout=settings.http_timeout,
            )
        )
        search = SearchClient(client=search_http)
        documents = DocumentsClient(client=documents_http)

        yield Runtime(
            chat=build_chat_service(
                settings,
                search=search,
                documents=documents,
            ),
            documents=documents,
            search=search,
        )
