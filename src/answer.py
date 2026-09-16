from typing import Any


def build_answer(
    question: str,
    retrieval_results: list[dict[str, Any]],
) -> dict[str, Any]:
    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "retrieved_cards": [],
        }

    if not retrieval_results:
        return {
            "answer": (
                "No relevant knowledge was found for this question."
            ),
            "sources": [],
            "retrieved_cards": [],
        }

    top_result = retrieval_results[0]
    top_card = top_result["card"]

    answer_text = top_card["content"]

    sources = [
        {
            "id": top_card["id"],
            "title": top_card["title"],
            "source": top_card["source"],
        }
    ]

    retrieved_cards = [
        {
            "id": item["card"]["id"],
            "title": item["card"]["title"],
            "score": item["score"],
        }
        for item in retrieval_results
    ]

    return {
        "answer": answer_text,
        "sources": sources,
        "retrieved_cards": retrieved_cards,
    }
