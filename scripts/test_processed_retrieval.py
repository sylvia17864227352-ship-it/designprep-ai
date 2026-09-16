from src.loader import load_processed_knowledge_cards
from src.retriever import retrieve_processed


cards = load_processed_knowledge_cards(
    "data/knowledge/processed/knowledge_cards.json"
)

questions = [
    "霍尔塔的代表作品是什么？",
    "什么是比利时线条？",
    "量子计算机的工作原理是什么？",
]

for question in questions:
    print("=" * 60)
    print("QUESTION:", question)

    results = retrieve_processed(
        question,
        cards,
    )

    if not results:
        print("NO RESULT")
        continue

    for item in results:
        card = item["card"]

        print(
            item["score"],
            card["id"],
            card.get("legacy_id"),
            card["name"],
        )
