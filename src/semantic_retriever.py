from typing import Any

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class SemanticRetriever:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.cards = []
        self.embeddings = None

    def build_index(
        self,
        cards: list[dict[str, Any]],
    ) -> None:
        self.cards = cards

        texts = [
            self._card_to_text(card)
            for card in cards
        ]

        self.embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

    def _card_to_text(
        self,
        card: dict[str, Any],
    ) -> str:
        parts = [
            card.get("name", ""),
            " ".join(
                card.get("aliases_keywords", [])
            ),
            " ".join(
                card.get("questions", [])
            ),
            card.get("standard_answer", ""),
            " ".join(
                card.get("memory_points", [])
            ),
        ]

        return "\n".join(
            part
            for part in parts
            if part
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
        min_score: float = 0.35,
    ) -> list[dict[str, Any]]:
        if not question.strip():
            return []

        if self.embeddings is None:
            raise RuntimeError(
                "Semantic index has not been built."
            )

        question_embedding = self.model.encode(
            question,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        scores = cos_sim(
            question_embedding,
            self.embeddings,
        )[0]

        ranked_indices = scores.argsort(
            descending=True
        )

        results = []
        seen_names = set()

        for index in ranked_indices:
            score = float(scores[index])

            if score < min_score:
                continue

            card = self.cards[int(index)]
            name = card.get("name", "").strip()

            if name in seen_names:
                continue

            seen_names.add(name)

            results.append(
                {
                    "score": score,
                    "card": card,
                }
            )

            if len(results) >= top_k:
                break

        return results
