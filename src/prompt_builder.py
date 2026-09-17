from typing import Any


SYSTEM_PROMPT = """
你是一个设计史知识问答助手。

你只能依据提供的知识库上下文回答问题。

回答要求：
1. 优先直接回答用户问题。
2. 不要使用上下文之外的事实。
3. 如果上下文不足以支持答案，明确回答“当前知识库中没有足够信息确认”。
4. 不要编造人物、作品、年代或来源。
5. 回答应简洁、准确，适合考研复习。
6. 如果上下文中存在多个相关知识点，只使用与问题最相关的信息。
""".strip()


def build_rag_messages(
    question: str,
    context_result: dict[str, Any],
) -> list[dict[str, str]]:
    context = context_result.get("context", "").strip()

    if not context:
        user_content = (
            f"问题：{question}\n\n"
            "知识库上下文为空。"
        )
    else:
        user_content = (
            f"问题：{question}\n\n"
            f"知识库上下文：\n{context}"
        )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]
