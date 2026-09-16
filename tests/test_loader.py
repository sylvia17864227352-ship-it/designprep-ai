import json

import pytest

from src.loader import load_knowledge_cards


def test_load_valid_knowledge_cards():
    cards = load_knowledge_cards("data/knowledge/sample_cards.json")

    assert len(cards) == 3
    assert cards[0]["id"] == "DS-001"
    assert cards[0]["title"] == "Bauhaus"


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_knowledge_cards("data/knowledge/not_exist.json")


def test_missing_required_field_raises_error(tmp_path):
    invalid_cards = [
        {
            "id": "DS-999",
            "title": "Invalid Card",
            "content": "Test content",
            "keywords": ["test"],
            "category": "test"
        }
    ]

    file_path = tmp_path / "invalid_cards.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(invalid_cards, file)

    with pytest.raises(ValueError, match="missing required fields"):
        load_knowledge_cards(file_path)


def test_duplicate_id_raises_error(tmp_path):
    duplicate_cards = [
        {
            "id": "DS-001",
            "title": "Card One",
            "content": "Content one",
            "keywords": ["one"],
            "category": "test",
            "source": "Test Source"
        },
        {
            "id": "DS-001",
            "title": "Card Two",
            "content": "Content two",
            "keywords": ["two"],
            "category": "test",
            "source": "Test Source"
        }
    ]

    file_path = tmp_path / "duplicate_cards.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(duplicate_cards, file)

    with pytest.raises(ValueError, match="Duplicate knowledge card ID"):
        load_knowledge_cards(file_path)
