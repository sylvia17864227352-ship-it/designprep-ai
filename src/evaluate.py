import json
from pathlib import Path

from src.loader import load_knowledge_cards
from src.retriever import retrieve


def load_evaluation_cases(file_path: str | Path) -> list[dict]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        cases = json.load(file)

    if not isinstance(cases, list):
        raise ValueError("Evaluation file must contain a JSON list.")

    return cases


def run_evaluation(
    knowledge_path: str | Path,
    evaluation_path: str | Path,
) -> dict:
    cards = load_knowledge_cards(knowledge_path)
    cases = load_evaluation_cases(evaluation_path)

    correct = 0
    results = []

    for case in cases:
        retrieval_results = retrieve(
            case["question"],
            cards,
            top_k=1,
        )

        predicted_id = None

        if retrieval_results:
            predicted_id = retrieval_results[0]["card"]["id"]

        passed = predicted_id == case["expected_card_id"]

        if passed:
            correct += 1

        results.append(
            {
                "id": case["id"],
                "question": case["question"],
                "expected_card_id": case["expected_card_id"],
                "predicted_card_id": predicted_id,
                "passed": passed,
            }
        )

    total = len(cases)
    accuracy = correct / total if total > 0 else 0.0

    return {
        "correct": correct,
        "total": total,
        "top1_accuracy": accuracy,
        "results": results,
    }


def main():
    report = run_evaluation(
        "data/knowledge/sample_cards.json",
        "data/evaluation.json",
    )

    print("Evaluation Results")
    print("------------------")

    for item in report["results"]:
        status = "PASS" if item["passed"] else "FAIL"

        print(
            f'{item["id"]} {status} '
            f'(expected={item["expected_card_id"]}, '
            f'predicted={item["predicted_card_id"]})'
        )

    print()
    print(
        f'Top-1 Accuracy: '
        f'{report["top1_accuracy"] * 100:.1f}%'
    )
    print(
        f'{report["correct"]} / '
        f'{report["total"]} correct'
    )


if __name__ == "__main__":
    main()
