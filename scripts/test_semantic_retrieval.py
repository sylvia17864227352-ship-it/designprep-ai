from src.loader import (
    load_processed_knowledge_cards,
)
from src.semantic_retriever import (
    SemanticRetriever,
)


cards = load_processed_knowledge_cards(
    "data/knowledge/processed/knowledge_cards.json"
)

retriever = SemanticRetriever()

print(
    f"Building semantic index "
    f"for {len(cards)} cards..."
)

retriever.build_index(cards)

questions = [
    "霍尔塔的代表作品是什么？",
    "霍尔塔最有名的建筑是哪一个？",
    "什么是比利时线条？",
    "量子计算机的工作原理是什么？",
]


for question in questions:
    print("=" * 60)
    print("QUESTION:", question)

    results = retriever.retrieve(
        question,
        top_k=3,
    )

    if not results:
        print("NO RESULT")
        continue

    for item in results:
        card = item["card"]

        print(
            f'{item["score"]:.4f}',
            card["id"],
            card.get("legacy_id"),
            card["name"],
        )
