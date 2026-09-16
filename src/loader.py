import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "id",
    "title",
    "content",
    "keywords",
    "category",
    "source",
}


def validate_card(card: dict[str, Any]) -> None:
    missing_fields = REQUIRED_FIELDS - card.keys()

    if missing_fields:
        raise ValueError(
            f"Knowledge card is missing required fields: "
            f"{', '.join(sorted(missing_fields))}"
        )

    if not isinstance(card["keywords"], list):
        raise ValueError(
            f"Knowledge card {card['id']} has invalid keywords field."
        )


def load_knowledge_cards(file_path: str | Path) -> list[dict[str, Any]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        cards = json.load(file)

    if not isinstance(cards, list):
        raise ValueError(
            "Knowledge file must contain a JSON list."
        )

    seen_ids = set()

    for card in cards:
        if not isinstance(card, dict):
            raise ValueError(
                "Each knowledge card must be a JSON object."
            )

        validate_card(card)

        if card["id"] in seen_ids:
            raise ValueError(
                f"Duplicate knowledge card ID: {card['id']}"
            )

        seen_ids.add(card["id"])

    return cards


PROCESSED_REQUIRED_FIELDS = {
    "id",
    "name",
    "knowledge_type",
    "subject",
    "aliases_keywords",
    "questions",
    "standard_answer",
    "memory_points",
    "source",
    "evidence",
    "review_status",
}


def validate_processed_card(card: dict[str, Any]) -> None:
    missing_fields = PROCESSED_REQUIRED_FIELDS - card.keys()

    if missing_fields:
        raise ValueError(
            "Processed knowledge card is missing required fields: "
            + ", ".join(sorted(missing_fields))
        )

    if not isinstance(card["aliases_keywords"], list):
        raise ValueError(
            f"Knowledge card {card['id']} has invalid aliases_keywords."
        )

    if not isinstance(card["questions"], list):
        raise ValueError(
            f"Knowledge card {card['id']} has invalid questions."
        )

    if not isinstance(card["memory_points"], list):
        raise ValueError(
            f"Knowledge card {card['id']} has invalid memory_points."
        )


def load_processed_knowledge_cards(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Processed knowledge file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        cards = json.load(file)

    if not isinstance(cards, list):
        raise ValueError(
            "Processed knowledge file must contain a JSON list."
        )

    seen_ids = set()

    for card in cards:
        if not isinstance(card, dict):
            raise ValueError(
                "Each processed knowledge card must be a JSON object."
            )

        validate_processed_card(card)

        if card["id"] in seen_ids:
            raise ValueError(
                f"Duplicate knowledge card ID: {card['id']}"
            )

        seen_ids.add(card["id"])

    return cards
