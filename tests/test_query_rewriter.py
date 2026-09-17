from src.query_rewriter import QueryRewriter


class FakeLLM:
    def __init__(self, response: str):
        self.response = response
        self.last_messages = None
        self.last_temperature = None

    def generate(
        self,
        messages,
        temperature=0.0,
    ):
        self.last_messages = messages
        self.last_temperature = temperature
        return self.response


def test_returns_original_question_without_history():
    llm = FakeLLM(
        "这条结果不应该被调用"
    )

    rewriter = QueryRewriter(
        llm=llm,
    )

    question = "霍尔塔是谁？"

    result = rewriter.rewrite(
        question,
        history=[],
    )

    assert result == question
    assert llm.last_messages is None


def test_rewrites_pronoun_using_active_topic():
    llm = FakeLLM(
        "霍尔塔（维克多·霍塔）的代表作品是什么？"
    )

    rewriter = QueryRewriter(
        llm=llm,
    )

    history = [
        {
            "role": "user",
            "content": "霍尔塔是谁？",
        },
        {
            "role": "assistant",
            "content": "霍尔塔是比利时新艺术运动的重要人物。",
            "active_topic": "霍尔塔（维克多·霍塔）",
        },
    ]

    result = rewriter.rewrite(
        "那他的代表作品呢？",
        history=history,
    )

    assert (
        result
        == "霍尔塔（维克多·霍塔）的代表作品是什么？"
    )


def test_active_topic_is_included_in_rewrite_prompt():
    llm = FakeLLM(
        "德国工业同盟有什么影响？"
    )

    rewriter = QueryRewriter(
        llm=llm,
    )

    history = [
        {
            "role": "assistant",
            "content": "德国工业同盟是德国现代设计史的重要组织。",
            "active_topic": "德国工业同盟",
        }
    ]

    rewriter.rewrite(
        "它有什么影响？",
        history=history,
    )

    user_message = llm.last_messages[1][
        "content"
    ]

    assert "当前主题：德国工业同盟" in user_message
    assert "它有什么影响？" in user_message


def test_uses_latest_active_topic():
    llm = FakeLLM(
        "勒·柯布西耶的设计理念是什么？"
    )

    rewriter = QueryRewriter(
        llm=llm,
    )

    history = [
        {
            "role": "assistant",
            "content": "霍尔塔相关回答",
            "active_topic": "霍尔塔",
        },
        {
            "role": "assistant",
            "content": "勒·柯布西耶相关回答",
            "active_topic": "勒·柯布西耶",
        },
    ]

    rewriter.rewrite(
        "他的设计理念是什么？",
        history=history,
    )

    user_message = llm.last_messages[1][
        "content"
    ]

    assert "当前主题：勒·柯布西耶" in user_message
