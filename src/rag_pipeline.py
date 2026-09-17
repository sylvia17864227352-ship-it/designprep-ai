from typing import Any

from src.context_builder import build_context
from src.hybrid_retriever import HybridRetriever
from src.llm_provider import LLMProvider
from src.prompt_builder import build_rag_messages


class RAGPipeline:
    def __init__(
        self,
        cards: list[dict[str, Any]],
        retriever: HybridRetriever,
        llm: LLMProvider,
    ):
        self.cards = cards
        self.retriever = retriever
        self.llm = llm

        self.retriever.build_index(cards)

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> dict[str, Any]:
        if not question.strip():
            return {
                "answer": "请输入问题。",
                "sources": [],
                "retrieval_results": [],
            }

        retrieval_results = self.retriever.retrieve(
            question,
            top_k=top_k,
        )

        if not retrieval_results:
            return {
                "answer": "当前知识库中没有足够信息确认。",
                "sources": [],
                "retrieval_results": [],
            }

        context_result = build_context(
            retrieval_results,
            max_cards=top_k,
        )

        messages = build_rag_messages(
            question,
            context_result,
        )

        answer = self.llm.generate(messages)

        return {
            "answer": answer,
            "sources": context_result["sources"],
            "retrieval_results": retrieval_results,
        }
