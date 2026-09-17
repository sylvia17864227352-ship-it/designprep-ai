from src.hybrid_retriever import HybridRetriever
from src.llm_provider import LLMProvider
from src.loader import load_processed_knowledge_cards
from src.rag_pipeline import RAGPipeline


KNOWLEDGE_PATH = (
    "data/knowledge/processed/knowledge_cards.json"
)


def main():
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

    questions = [
        "霍尔塔的代表作品是什么？",
        "谁被称为第一个驻厂设计师？",
        "量子计算机的工作原理是什么？",
    ]

    for question in questions:
        print("=" * 60)
        print("QUESTION:", question)

        result = pipeline.ask(question)

        print()
        print("ANSWER:")
        print(result["answer"])

        print()
        print("SOURCES:")

        if not result["sources"]:
            print("NO SOURCE")
        else:
            for source in result["sources"]:
                print(
                    source["card_id"],
                    source["name"],
                    source["source"],
                )


if __name__ == "__main__":
    main()
