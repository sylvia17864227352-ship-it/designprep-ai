from typing import Any

from src.retriever import calculate_processed_score
from src.semantic_retriever import SemanticRetriever


class HybridRetriever:
    def __init__(
        self,
        keyword_weight: float = 0.7,
        semantic_weight: float = 0.3,
    ):
        self.keyword_weight = keyword_weight
        self.semantic_weight = semantic_weight
        self.semantic = SemanticRetriever()
        self.cards = []

    def build_index(
        self,
        cards: list[dict[str, Any]],
    ) -> None:
        self.cards = cards
        self.semantic.build_index(cards)

    def _normalize_keyword_scores(
        self,
        question: str,
    ) -> dict[str, float]:
        raw_scores = {}

        for card in self.cards:
            score = calculate_processed_score(
                question,
                card,
            )

            raw_scores[card["id"]] = float(score)

        max_score = max(
            raw_scores.values(),
            default=0.0,
        )

        if max_score <= 0:
            return {
                card_id: 0.0
                for card_id in raw_scores
            }

        return {
            card_id: score / max_score
            for card_id, score in raw_scores.items()
        }

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
        min_keyword_score: int = 20,
        min_semantic_score: float = 0.35,
        min_hybrid_score: float = 0.30,
    ) -> list[dict[str, Any]]:
        if not question.strip():
            return []

        keyword_scores = self._normalize_keyword_scores(
            question
        )

        semantic_results = self.semantic.retrieve(
            question,
            top_k=len(self.cards),
            min_score=0.0,
        )

        semantic_scores = {
            item["card"]["id"]: item["score"]
            for item in semantic_results
        }

        candidates = []

        for card in self.cards:
            card_id = card["id"]

            raw_keyword_score = calculate_processed_score(
                question,
                card,
            )

            semantic_score = semantic_scores.get(
                card_id,
                0.0,
            )

            keyword_score = keyword_scores.get(
                card_id,
                0.0,
            )

            if (
                raw_keyword_score < min_keyword_score
                and semantic_score < min_semantic_score
            ):
                continue

            hybrid_score = (
                self.keyword_weight * keyword_score
                + self.semantic_weight * semantic_score
            )

            if hybrid_score < min_hybrid_score:
                continue

            candidates.append(
                {
                    "score": hybrid_score,
                    "keyword_score": raw_keyword_score,
                    "semantic_score": semantic_score,
                    "card": card,
                }
            )

        candidates.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        unique_results = []
        seen_names = set()

        for item in candidates:
            name = item["card"].get(
                "name",
                "",
            ).strip()

            if name in seen_names:
                continue

            seen_names.add(name)
            unique_results.append(item)

            if len(unique_results) >= top_k:
                break

        return unique_results
