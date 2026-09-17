import html

import streamlit as st

from src.hybrid_retriever import HybridRetriever
from src.llm_provider import LLMProvider
from src.loader import load_processed_knowledge_cards
from src.rag_pipeline import RAGPipeline


KNOWLEDGE_PATH = (
    "data/knowledge/processed/knowledge_cards.json"
)


@st.cache_resource
def build_pipeline():
    cards = load_processed_knowledge_cards(
        KNOWLEDGE_PATH
    )

    retriever = HybridRetriever(
        keyword_weight=0.7,
        semantic_weight=0.3,
    )

    llm = LLMProvider()

    pipeline = RAGPipeline(
        cards=cards,
        retriever=retriever,
        llm=llm,
    )

    return pipeline, len(cards)


def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def apply_style():
    st.markdown(
        """
        <style>

        .block-container {
            max-width: 950px;
            padding-top: 2rem;
            padding-bottom: 7rem;
        }

        .user-bubble {
            background: #f1f3f5;
            border-radius: 18px 18px 4px 18px;
            padding: 14px 18px;
            margin: 8px 0 18px 0;
            font-size: 17px;
            line-height: 1.7;
            display: inline-block;
            max-width: 100%;
            text-align: left;
        }

        .assistant-bubble {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 18px 18px 18px 4px;
            padding: 14px 18px;
            margin: 8px 0 8px 0;
            font-size: 17px;
            line-height: 1.7;
            display: inline-block;
            max-width: 100%;
        }

        .user-label {
            text-align: right;
            color: #8b5cf6;
            font-size: 13px;
            margin-bottom: -4px;
        }

        .assistant-label {
            color: #f59e0b;
            font-size: 13px;
            margin-bottom: -4px;
        }

        .designprep-subtitle {
            color: #6b7280;
            margin-bottom: 0.25rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources):
    if not sources:
        return

    with st.expander("查看资料来源"):
        for source in sources:
            source_info = source.get(
                "source",
                {},
            )

            name = source.get(
                "name",
                "",
            )

            card_id = source.get(
                "card_id",
                "",
            )

            book = source_info.get(
                "book",
                "未知来源",
            )

            page = source_info.get(
                "page",
            )

            source_text = (
                f"**{name}**  \n"
                f"知识卡：`{card_id}`  \n"
                f"来源：{book}"
            )

            if page:
                source_text += f"，第 {page} 页"

            st.markdown(source_text)


def render_rewritten_query(
    original_question,
    rewritten_question,
):
    if not original_question:
        return

    if not rewritten_question:
        return

    with st.expander("查看检索问题"):
        st.markdown(
            f"**原始问题：** {original_question}"
        )

        st.markdown(
            f"**改写后：** {rewritten_question}"
        )


def render_timings(timings_ms):
    if not timings_ms:
        return

    with st.expander("查看性能信息"):
        rewrite_ms = timings_ms.get(
            "rewrite",
            0,
        )

        retrieval_ms = timings_ms.get(
            "retrieval",
            0,
        )

        generation_ms = timings_ms.get(
            "generation",
            0,
        )

        total_ms = timings_ms.get(
            "total",
            0,
        )

        st.markdown(
            f"""
- Query Rewrite: `{rewrite_ms} ms`
- Retrieval: `{retrieval_ms} ms`
- Generation: `{generation_ms} ms`
- Total: `{total_ms} ms`
            """
        )


def render_user_message(content):
    left_space, user_column = st.columns(
        [0.28, 0.72]
    )

    with user_column:
        st.markdown(
            '<div class="user-label">你</div>',
            unsafe_allow_html=True,
        )

        safe_content = html.escape(content)

        safe_content = safe_content.replace(
            "\n",
            "<br>",
        )

        st.markdown(
            f"""
            <div style="text-align:right;">
                <div class="user-bubble">
                    {safe_content}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_assistant_message(
    content,
    sources=None,
    original_question=None,
    rewritten_question=None,
    timings_ms=None,
):
    assistant_column, right_space = st.columns(
        [0.78, 0.22]
    )

    with assistant_column:
        st.markdown(
            '<div class="assistant-label">'
            'DesignPrep AI'
            '</div>',
            unsafe_allow_html=True,
        )

        safe_content = html.escape(content)

        safe_content = safe_content.replace(
            "\n",
            "<br>",
        )

        st.markdown(
            f"""
            <div class="assistant-bubble">
                {safe_content}
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_rewritten_query(
            original_question,
            rewritten_question,
        )

        render_timings(
            timings_ms or {}
        )

        render_sources(
            sources or []
        )


def render_history():
    for message in st.session_state.messages:
        role = message.get(
            "role",
            "",
        )

        if role == "user":
            render_user_message(
                message.get(
                    "content",
                    "",
                )
            )

        elif role == "assistant":
            render_assistant_message(
                message.get(
                    "content",
                    "",
                ),
                sources=message.get(
                    "sources",
                    [],
                ),
                original_question=message.get(
                    "original_question",
                ),
                rewritten_question=message.get(
                    "rewritten_question",
                ),
                timings_ms=message.get(
                    "timings_ms",
                    {},
                ),
            )


def main():
    st.set_page_config(
        page_title="DesignPrep AI",
        page_icon="📚",
        layout="centered",
    )

    apply_style()
    initialize_chat()

    st.title("DesignPrep AI")

    st.markdown(
        '<div class="designprep-subtitle">'
        "基于设计史知识库的可追溯 AI 问答助手"
        "</div>",
        unsafe_allow_html=True,
    )

    try:
        pipeline, card_count = build_pipeline()

    except Exception as error:
        st.error(
            f"系统初始化失败：{error}"
        )
        return

    st.caption(
        f"当前已加载 {card_count} 张知识卡"
    )

    st.divider()

    render_history()

    question = st.chat_input(
        "输入你的设计史问题..."
    )

    if not question:
        return

    history = list(
        st.session_state.messages
    )

    render_user_message(
        question
    )

    with st.spinner(
        "正在检索知识库并生成回答..."
    ):
        try:
            result = pipeline.ask(
                question,
                history=history,
            )

        except Exception as error:
            st.error(
                f"回答生成失败：{error}"
            )
            return

    rewritten_question = result.get(
        "rewritten_question",
        question,
    )

    sources = result.get(
        "sources",
        [],
    )

    active_topic = result.get(
        "active_topic",
        "",
    )

    timings_ms = result.get(
        "timings_ms",
        {},
    )

    render_assistant_message(
        result["answer"],
        sources=sources,
        original_question=question,
        rewritten_question=rewritten_question,
        timings_ms=timings_ms,
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": sources,
            "original_question": question,
            "rewritten_question": rewritten_question,
            "active_topic": active_topic,
            "timings_ms": timings_ms,
        }
    )


if __name__ == "__main__":
    main()
