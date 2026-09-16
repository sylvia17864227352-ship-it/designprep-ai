from src.loader import load_knowledge_cards
from src.retriever import retrieve


def test_retrieve_bauhaus():
    cards = load_knowledge_cards(
        "data/knowledge/sample_cards.json"
    )

    results = retrieve(
        "Who founded the Bauhaus?",
        cards,
    )

    assert len(results) > 0
    assert results[0]["card"]["id"] == "DS-001"


def test_retrieve_arts_and_crafts():
    cards = load_knowledge_cards(
        "data/knowledge/sample_cards.json"
    )

    results = retrieve(
        "What did William Morris criticize?",
        cards,
    )

    assert len(results) > 0
    assert results[0]["card"]["id"] == "DS-002"


def test_retrieve_ulm():
    cards = load_knowledge_cards(
        "data/knowledge/sample_cards.json"
    )

    results = retrieve(
        "Which school emphasized systematic design methods?",
        cards,
    )

    assert len(results) > 0
    assert results[0]["card"]["id"] == "DS-003"


def test_empty_question_returns_empty_results():
    cards = load_knowledge_cards(
        "data/knowledge/sample_cards.json"
    )

    results = retrieve("", cards)

    assert results == []
