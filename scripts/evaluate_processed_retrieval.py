import json

from src.loader import load_processed_knowledge_cards
from src.retriever import retrieve_processed


KNOWLEDGE_PATH = "data/knowledge/processed/knowledge_cards.json"
EVAL_PATH = "data/evaluation_zh.json"


def main():
    cards = load_processed_knowledge_cards(KNOWLEDGE_PATH)

    with open(EVAL_PATH, "r", encoding="utf-8") as file:
        cases = json.load(file)

    hit1 = 0
    hit3 = 0
    no_answer_correct = 0
    no_answer_total = 0

    print("Chinese Retrieval Evaluation")
    print("=" * 60)

    for case in cases:
        results = retrieve_processed(
            case["question"],
            cards,
            top_k=3,
        )

        expected = case["expected_legacy_id"]

        predicted_ids = [
            item["card"].get("legacy_id")
            for item in results
        ]

        if expected is None:
            no_answer_total += 1
            passed = len(results) == 0

            if passed:
                no_answer_correct += 1

            print(
                case["id"],
                "PASS" if passed else "FAIL",
                "| expected=None",
                "| predicted=",
                predicted_ids,
            )

            continue

        top1_correct = (
            len(predicted_ids) > 0
            and predicted_ids[0] == expected
        )

        top3_correct = expected in predicted_ids[:3]

        if top1_correct:
            hit1 += 1

        if top3_correct:
            hit3 += 1

        print(
            case["id"],
            "| expected=",
            expected,
            "| predicted=",
            predicted_ids,
        )

    positive_total = sum(
        1
        for case in cases
        if case["expected_legacy_id"] is not None
    )

    print()
    print("Results")
    print("-" * 60)

    if positive_total:
        print(
            f"Hit@1: {hit1}/{positive_total} "
            f"({hit1 / positive_total * 100:.1f}%)"
        )

        print(
            f"Hit@3: {hit3}/{positive_total} "
            f"({hit3 / positive_total * 100:.1f}%)"
        )

    if no_answer_total:
        print(
            f"No-answer accuracy: "
            f"{no_answer_correct}/{no_answer_total} "
            f"({no_answer_correct / no_answer_total * 100:.1f}%)"
        )


if __name__ == "__main__":
    main()
