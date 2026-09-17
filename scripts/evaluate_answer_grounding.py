import json

from src.hybrid_retriever import HybridRetriever
from src.llm_provider import LLMProvider
from src.loader import load_processed_knowledge_cards
from src.rag_pipeline import RAGPipeline


KNOWLEDGE_PATH = (
    "data/knowledge/processed/knowledge_cards.json"
)

EVAL_PATH = (
    "data/evaluation_answer_grounding.json"
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

    with open(
        EVAL_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    passed = 0

    print("Answer Grounding Evaluation")
    print("=" * 60)

    for case in cases:
        result = pipeline.ask(
            case["question"]
        )

        answer = result["answer"]

        expected_ok = all(
            keyword in answer
            for keyword
            in case["expected_keywords"]
        )

        forbidden_ok = all(
            keyword not in answer
            for keyword
            in case["forbidden_keywords"]
        )

        is_passed = (
            expected_ok
            and forbidden_ok
        )

        if is_passed:
            passed += 1

        print()
        print(case["id"])
        print("Question:", case["question"])
        print("Answer  :", answer)
        print(
            "Result  :",
            "PASS" if is_passed else "FAIL",
        )

    total = len(cases)

    print()
    print("=" * 60)

    print(
        f"Passed: {passed}/{total} "
        f"({passed / total * 100:.1f}%)"
    )


if __name__ == "__main__":
    main()
