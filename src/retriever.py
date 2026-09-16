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
    min_score: int = 2,
) -> list[dict[str, Any]]:
    if not question.strip():
        return []

    scored_cards = []

    for card in cards:
        score = calculate_score(question, card)

        if score >= min_score:
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


def tokenize_mixed(text: str) -> set[str]:
    text = normalize_text(text)

    english_tokens = set(
        re.findall(r"[a-zA-Z0-9]+", text)
    )

    chinese_sequences = re.findall(
        r"[\u4e00-\u9fff]+",
        text,
    )

    chinese_tokens = set()

    for sequence in chinese_sequences:
        if len(sequence) == 1:
            chinese_tokens.add(sequence)
            continue

        for i in range(len(sequence) - 1):
            chinese_tokens.add(sequence[i:i + 2])

    return english_tokens | chinese_tokens


def calculate_processed_score(
    question: str,
    card: dict[str, Any],
) -> int:
    question_tokens = tokenize_mixed(question)

    if not question_tokens:
        return 0

    name_tokens = tokenize_mixed(
        card.get("name", "")
    )

    alias_tokens = set()
    for item in card.get("aliases_keywords", []):
        alias_tokens.update(
            tokenize_mixed(item)
        )

    question_example_tokens = set()
    for item in card.get("questions", []):
        question_example_tokens.update(
            tokenize_mixed(item)
        )

    answer_tokens = tokenize_mixed(
        card.get("standard_answer", "")
    )

    memory_tokens = set()
    for item in card.get("memory_points", []):
        memory_tokens.update(
            tokenize_mixed(item)
        )

    evidence_tokens = tokenize_mixed(
        card.get("evidence", "")
    )

    score = 0

    score += len(question_tokens & name_tokens) * 5
    score += len(question_tokens & alias_tokens) * 4
    score += len(question_tokens & question_example_tokens) * 3
    score += len(question_tokens & answer_tokens) * 2
    score += len(question_tokens & memory_tokens)
    score += len(question_tokens & evidence_tokens)

    return score


def retrieve_processed(
    question: str,
    cards: list[dict[str, Any]],
    top_k: int = 3,
    min_score: int = 20,
) -> list[dict[str, Any]]:
    if not question.strip():
        return []

    scored_cards = []

    for card in cards:
        score = calculate_processed_score(question, card)

        if score >= min_score:
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

    unique_results = []
    seen_names = set()

    for item in scored_cards:
        name = item["card"].get("name", "").strip()

        if name in seen_names:
            continue

        seen_names.add(name)
        unique_results.append(item)

        if len(unique_results) >= top_k:
            break

    return unique_results
