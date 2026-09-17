from typing import Any

from src.llm_provider import LLMProvider


REWRITE_SYSTEM_PROMPT = """
你是设计史知识库的查询改写助手。

你的任务不是回答问题，而是把当前用户问题改写成一个独立、
明确、可以直接用于知识库检索的问题。

规则：
1. 只输出改写后的问题。
2. 不回答问题。
3. 如果当前问题已经完整独立，尽量原样返回。
4. 如果问题出现“他、她、它、这个、那个、该人物、该运动、
   其、这种”等指代，应优先使用提供的“当前主题”进行补全。
5. 当前主题优先级高于更早的历史对话。
6. 不要引入当前主题和历史中不存在的新人物或知识。
""".strip()


class QueryRewriter:
    def __init__(
        self,
        llm: LLMProvider,
        max_history_messages: int = 4,
    ):
        self.llm = llm
        self.max_history_messages = max_history_messages

    def _find_active_topic(
        self,
        history: list[dict[str, Any]],
    ) -> str:
        for message in reversed(history):
            if message.get("role") != "assistant":
                continue

            topic = message.get(
                "active_topic",
                "",
            ).strip()

            if topic:
                return topic

        return ""

    def rewrite(
        self,
        question: str,
        history: list[dict[str, Any]],
    ) -> str:
        question = question.strip()

        if not question:
            return ""

        if not history:
            return question

        active_topic = self._find_active_topic(
            history
        )

        recent_history = history[
            -self.max_history_messages:
        ]

        history_text = []

        for message in recent_history:
            role = message.get(
                "role",
                "",
            )

            content = message.get(
                "content",
                "",
            )

            history_text.append(
                f"{role}: {content}"
            )

        topic_text = (
            active_topic
            if active_topic
            else "无明确当前主题"
        )

        messages = [
            {
                "role": "system",
                "content": REWRITE_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"当前主题：{topic_text}\n\n"
                    "最近对话：\n"
                    + "\n".join(history_text)
                    + "\n\n当前用户问题：\n"
                    + question
                ),
            },
        ]

        rewritten = self.llm.generate(
            messages,
            temperature=0.0,
        )

        return (
            rewritten.strip()
            or question
        )
