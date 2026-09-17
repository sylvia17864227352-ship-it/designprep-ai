from typing import Any


def build_context(
    retrieval_results: list[dict[str, Any]],
    max_cards: int = 3,
) -> dict[str, Any]:
    if not retrieval_results:
        return {
            "context": "",
            "sources": [],
        }

    context_blocks = []
    sources = []

    for index, item in enumerate(
        retrieval_results[:max_cards],
        start=1,
    ):
        card = item["card"]

        name = card.get("name", "")
        answer = card.get("standard_answer", "")
        evidence = card.get("evidence", "")
        source = card.get("source", {})
        card_id = card.get("id", "")

        context_block = (
            f"[Knowledge {index}]\n"
            f"Card ID: {card_id}\n"
            f"Topic: {name}\n"
            f"Standard Answer: {answer}\n"
            f"Evidence: {evidence}\n"
        )

        context_blocks.append(context_block)

        sources.append(
            {
                "card_id": card_id,
                "name": name,
                "source": source,
            }
        )

    return {
        "context": "\n".join(context_blocks),
        "sources": sources,
    }
