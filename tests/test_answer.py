from src.answer import build_answer


def test_build_answer_from_retrieval_result():
    retrieval_results = [
        {
            "score": 7,
            "card": {
                "id": "DS-001",
                "title": "Bauhaus",
                "content": (
                    "The Bauhaus was founded by Walter Gropius "
                    "in Weimar in 1919."
                ),
                "keywords": ["Bauhaus", "Walter Gropius"],
                "category": "design_movement",
                "source": "Design History Notes",
            },
        }
    ]

    result = build_answer(
        "Who founded the Bauhaus?",
        retrieval_results,
    )

    assert "Walter Gropius" in result["answer"]
    assert result["sources"][0]["id"] == "DS-001"
    assert result["retrieved_cards"][0]["score"] == 7


def test_empty_question_returns_prompt():
    result = build_answer("", [])

    assert result["answer"] == "Please enter a question."
    assert result["sources"] == []


def test_no_retrieval_result_returns_fallback():
    result = build_answer(
        "Unknown question",
        [],
    )

    assert (
        result["answer"]
        == "No relevant knowledge was found for this question."
    )
    assert result["sources"] == []
