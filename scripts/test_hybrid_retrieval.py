from src.loader import load_processed_knowledge_cards
from src.hybrid_retriever import HybridRetriever


cards = load_processed_knowledge_cards(
    "data/knowledge/processed/knowledge_cards.json"
)

retriever = HybridRetriever(
    keyword_weight=0.7,
    semantic_weight=0.3,
)

print(
    f"Building hybrid index for {len(cards)} cards..."
)

retriever.build_index(cards)

questions = [
    "霍尔塔的代表作品是什么？",
    "霍尔塔最有名的建筑是哪一个？",
    "什么是比利时线条？",
    "谁被称为第一个驻厂设计师？",
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
            f'hybrid={item["score"]:.4f}',
            f'keyword={item["keyword_score"]}',
            f'semantic={item["semantic_score"]:.4f}',
            card["name"],
        )
