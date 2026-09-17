from src.prompt_builder import build_rag_messages


def test_build_rag_messages():
    context_result = {
        "context": (
            "[Knowledge 1]\n"
            "Topic: 霍尔塔\n"
            "Standard Answer: 霍尔塔是比利时新艺术运动的重要代表。"
        ),
        "sources": [],
    }

    messages = build_rag_messages(
        "霍尔塔是谁？",
        context_result,
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "霍尔塔是谁" in messages[1]["content"]
    assert "霍尔塔是比利时新艺术运动的重要代表" in messages[1]["content"]


def test_empty_context_is_explicit():
    messages = build_rag_messages(
        "一个不存在的问题",
        {
            "context": "",
            "sources": [],
        },
    )

    assert "知识库上下文为空" in messages[1]["content"]
