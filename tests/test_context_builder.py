from src.context_builder import build_context


def test_build_context():
    results = [
        {
            "score": 0.9,
            "card": {
                "id": "DS-0001",
                "name": "霍尔塔",
                "standard_answer": "霍尔塔是比利时新艺术运动的重要代表。",
                "evidence": "霍尔塔的建筑设计代表了比利时新艺术运动的重要发展。",
                "source": {
                    "book": "世界现代设计史",
                    "page": 22,
                },
            },
        }
    ]

    result = build_context(results)

    assert "霍尔塔" in result["context"]
    assert "DS-0001" in result["context"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["name"] == "霍尔塔"


def test_empty_results():
    result = build_context([])

    assert result["context"] == ""
    assert result["sources"] == []
