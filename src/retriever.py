import re
from typing import Any


def normalize_text(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str) -> set[str]:
    normalized = normalize_text(text)
    tokens = re.findall(r"[a-zA-Z0-9]+", normalized)
    return set(tokens)


def calculate_score(
    question: str,
    card: dict[str, Any],
) -> int:
    question_tokens = tokenize(question)

    if not question_tokens:
        return 0

    title_tokens = tokenize(card["title"])
    content_tokens = tokenize(card["content"])

    keyword_tokens = set()

    for keyword in card["keywords"]:
        keyword_tokens.update(tokenize(keyword))

    score = 0

    score += len(question_tokens & title_tokens) * 3
    score += len(question_tokens & keyword_tokens) * 2
    score += len(question_tokens & content_tokens)

    return score


def retrieve(
    question: str,
    cards: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    if not question.strip():
        return []

    scored_cards = []

    for card in cards:
        score = calculate_score(question, card)

        if score > 0:
            scored_cards.append(
                {
                    "score": score,
                    "card": card,
                }
            )

    scored_cards.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_cards[:top_k]
