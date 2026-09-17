from time import perf_counter
from typing import Any

from src.context_builder import build_context
from src.hybrid_retriever import HybridRetriever
from src.llm_provider import LLMProvider
from src.prompt_builder import build_rag_messages
from src.query_rewriter import QueryRewriter


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
        self.query_rewriter = QueryRewriter(llm)

        self.retriever.build_index(cards)

    def ask(
        self,
        question: str,
        history: list[dict[str, Any]] | None = None,
        top_k: int = 3,
    ) -> dict[str, Any]:
        total_start = perf_counter()

        if not question.strip():
            return {
                "answer": "请输入问题。",
                "sources": [],
                "retrieval_results": [],
                "rewritten_question": "",
                "active_topic": "",
                "timings_ms": {
                    "rewrite": 0.0,
                    "retrieval": 0.0,
                    "generation": 0.0,
                    "total": 0.0,
                },
            }

        history = history or []

        rewrite_start = perf_counter()

        rewritten_question = self.query_rewriter.rewrite(
            question,
            history,
        )

        rewrite_ms = (
            perf_counter() - rewrite_start
        ) * 1000

        retrieval_start = perf_counter()

        retrieval_results = self.retriever.retrieve(
            rewritten_question,
            top_k=top_k,
        )

        retrieval_ms = (
            perf_counter() - retrieval_start
        ) * 1000

        if not retrieval_results:
            total_ms = (
                perf_counter() - total_start
            ) * 1000

            return {
                "answer": "当前知识库中没有足够信息确认。",
                "sources": [],
                "retrieval_results": [],
                "rewritten_question": rewritten_question,
                "active_topic": "",
                "timings_ms": {
                    "rewrite": round(
                        rewrite_ms,
                        2,
                    ),
                    "retrieval": round(
                        retrieval_ms,
                        2,
                    ),
                    "generation": 0.0,
                    "total": round(
                        total_ms,
                        2,
                    ),
                },
            }

        context_result = build_context(
            retrieval_results,
            max_cards=top_k,
        )

        messages = build_rag_messages(
            rewritten_question,
            context_result,
        )

        generation_start = perf_counter()

        answer = self.llm.generate(
            messages
        )

        generation_ms = (
            perf_counter() - generation_start
        ) * 1000

        top_card = retrieval_results[0]["card"]

        total_ms = (
            perf_counter() - total_start
        ) * 1000

        return {
            "answer": answer,
            "sources": context_result["sources"],
            "retrieval_results": retrieval_results,
            "rewritten_question": rewritten_question,
            "active_topic": top_card.get(
                "name",
                "",
            ),
            "timings_ms": {
                "rewrite": round(
                    rewrite_ms,
                    2,
                ),
                "retrieval": round(
                    retrieval_ms,
                    2,
                ),
                "generation": round(
                    generation_ms,
                    2,
                ),
                "total": round(
                    total_ms,
                    2,
                ),
            },
        }
