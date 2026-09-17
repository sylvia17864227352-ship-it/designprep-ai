from typing import Any

from src import answer
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
        if not question.strip():
            return {
                "answer": "请输入问题。",
                "sources": [],
                "retrieval_results": [],
                "rewritten_question": "",
            }

        history = history or []

        rewritten_question = self.query_rewriter.rewrite(
            question,
            history,
        )

        retrieval_results = self.retriever.retrieve(
            rewritten_question,
            top_k=top_k,
        )

        if not retrieval_results:
            return {
                "answer": "当前知识库中没有足够信息确认。",
                "sources": [],
                "retrieval_results": [],
                "rewritten_question": rewritten_question,
            }

        context_result = build_context(
            retrieval_results,
            max_cards=top_k,
        )

        messages = build_rag_messages(
            rewritten_question,
            context_result,
        )

        answer = self.llm.generate(
            messages
        )

        top_card = retrieval_results[0]["card"]

        return {
            "answer": answer,
            "sources": context_result["sources"],
            "retrieval_results": retrieval_results,
            "rewritten_question": rewritten_question,
            "active_topic": top_card.get("name", ""),
        }
