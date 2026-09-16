import streamlit as st

from src.loader import load_knowledge_cards
from src.retriever import retrieve
from src.answer import build_answer


KNOWLEDGE_PATH = "data/knowledge/sample_cards.json"

EXAMPLE_QUESTIONS = [
    "Who founded the Bauhaus?",
    "What did William Morris criticize?",
    "Which school emphasized systematic design methods?",
]


@st.cache_data
def load_cards():
    return load_knowledge_cards(KNOWLEDGE_PATH)


def main():
    st.set_page_config(
        page_title="DesignPrep AI",
        page_icon="📚",
        layout="centered",
    )

    st.title("DesignPrep AI")
    st.caption(
        "A lightweight design-history question-answering assistant "
        "with source tracing."
    )

    try:
        cards = load_cards()
    except Exception as error:
        st.error(f"Failed to load knowledge data: {error}")
        return

    st.write(f"Knowledge cards loaded: {len(cards)}")

    st.subheader("Example questions")

    for example in EXAMPLE_QUESTIONS:
        st.code(example, language=None)

    question = st.text_input(
        "Ask a design history question",
        placeholder="e.g. Who founded the Bauhaus?",
    )

    if st.button("Ask", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        retrieval_results = retrieve(
            question,
            cards,
            top_k=3,
        )

        response = build_answer(
            question,
            retrieval_results,
        )

        st.divider()

        st.subheader("Answer")
        st.write(response["answer"])

        if response["sources"]:
            st.subheader("Source")

            for source in response["sources"]:
                st.markdown(
                    f'**{source["title"]}**  \n'
                    f'Card ID: `{source["id"]}`  \n'
                    f'Source: {source["source"]}'
                )

        else:
            st.info(
                "No source was returned because no relevant "
                "knowledge card was found."
            )

        if response["retrieved_cards"]:
            with st.expander("Retrieval details"):
                for index, card in enumerate(
                    response["retrieved_cards"],
                    start=1,
                ):
                    st.write(
                        f'{index}. {card["id"]} — '
                        f'{card["title"]} '
                        f'(score: {card["score"]})'
                    )


if __name__ == "__main__":
    main()
