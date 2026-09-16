import streamlit as st

from src.loader import load_knowledge_cards
from src.retriever import retrieve
from src.answer import build_answer


KNOWLEDGE_PATH = "data/knowledge/sample_cards.json"


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
    st.caption("Design history question-answering assistant")

    cards = load_cards()

    question = st.text_input(
        "Ask a design history question",
        placeholder="e.g. Who founded the Bauhaus?",
    )

    if st.button("Ask"):
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

        st.subheader("Answer")
        st.write(response["answer"])

        if response["sources"]:
            st.subheader("Source")

            for source in response["sources"]:
                st.write(
                    f'**{source["title"]}** '
                    f'({source["id"]})'
                )
                st.caption(source["source"])

        if response["retrieved_cards"]:
            with st.expander("Retrieval details"):
                for card in response["retrieved_cards"]:
                    st.write(
                        f'{card["id"]} · '
                        f'{card["title"]} · '
                        f'Score: {card["score"]}'
                    )


if __name__ == "__main__":
    main()
