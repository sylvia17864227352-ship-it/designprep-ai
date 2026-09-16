import json

from src.loader import load_processed_knowledge_cards
from src.retriever import retrieve_processed
from src.semantic_retriever import SemanticRetriever
from src.hybrid_retriever import HybridRetriever


KNOWLEDGE_PATH = "data/knowledge/processed/knowledge_cards.json"
EVAL_PATH = "data/evaluation_zh.json"


def evaluate_keyword(cards, cases):
    hit1 = 0
    hit3 = 0
    no_answer_correct = 0
    no_answer_total = 0
    positive_total = 0

    for case in cases:
        results = retrieve_processed(
            case["question"],
            cards,
            top_k=3,
        )

        predicted_names = [
            item["card"].get("name")
            for item in results
        ]

        expected = case["expected_name"]

        if expected is None:
            no_answer_total += 1

            if not results:
                no_answer_correct += 1

            print(
                case["id"],
                "| expected=None",
                "| predicted=",
                predicted_names,
            )
            continue

        positive_total += 1

        if predicted_names:
            if predicted_names[0] == expected:
                hit1 += 1

        if expected in predicted_names[:3]:
            hit3 += 1

        print(
            case["id"],
            "| expected=",
            expected,
            "| predicted=",
            predicted_names,
        )

    return {
        "hit1": hit1,
        "hit3": hit3,
        "positive_total": positive_total,
        "no_answer_correct": no_answer_correct,
        "no_answer_total": no_answer_total,
    }


def evaluate_semantic(cards, cases):
    retriever = SemanticRetriever()

    print()
    print("Building semantic index...")
    retriever.build_index(cards)

    hit1 = 0
    hit3 = 0
    no_answer_correct = 0
    no_answer_total = 0
    positive_total = 0

    for case in cases:
        results = retriever.retrieve(
            case["question"],
            top_k=3,
        )

        predicted_names = [
            item["card"].get("name")
            for item in results
        ]

        expected = case["expected_name"]

        if expected is None:
            no_answer_total += 1

            if not results:
                no_answer_correct += 1

            print(
                case["id"],
                "| expected=None",
                "| predicted=",
                predicted_names,
            )
            continue

        positive_total += 1

        if predicted_names:
            if predicted_names[0] == expected:
                hit1 += 1

        if expected in predicted_names[:3]:
            hit3 += 1

        print(
            case["id"],
            "| expected=",
            expected,
            "| predicted=",
            predicted_names,
        )

    return {
        "hit1": hit1,
        "hit3": hit3,
        "positive_total": positive_total,
        "no_answer_correct": no_answer_correct,
        "no_answer_total": no_answer_total,
    }


def evaluate_hybrid(cards, cases):
    retriever = HybridRetriever(
        keyword_weight=0.7,
        semantic_weight=0.3,
    )

    print()
    print("Building hybrid index...")
    retriever.build_index(cards)

    hit1 = 0
    hit3 = 0
    no_answer_correct = 0
    no_answer_total = 0
    positive_total = 0

    for case in cases:
        results = retriever.retrieve(
            case["question"],
            top_k=3,
        )

        predicted_names = [
            item["card"].get("name")
            for item in results
        ]

        expected = case["expected_name"]

        if expected is None:
            no_answer_total += 1

            if not results:
                no_answer_correct += 1

            print(
                case["id"],
                "| expected=None",
                "| predicted=",
                predicted_names,
            )
            continue

        positive_total += 1

        if predicted_names:
            if predicted_names[0] == expected:
                hit1 += 1

        if expected in predicted_names[:3]:
            hit3 += 1

        print(
            case["id"],
            "| expected=",
            expected,
            "| predicted=",
            predicted_names,
        )

    return {
        "hit1": hit1,
        "hit3": hit3,
        "positive_total": positive_total,
        "no_answer_correct": no_answer_correct,
        "no_answer_total": no_answer_total,
    }


def print_report(name, report):
    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    positive_total = report["positive_total"]

    if positive_total:
        print(
            f'Hit@1: {report["hit1"]}/{positive_total} '
            f'({report["hit1"] / positive_total * 100:.1f}%)'
        )

        print(
            f'Hit@3: {report["hit3"]}/{positive_total} '
            f'({report["hit3"] / positive_total * 100:.1f}%)'
        )

    no_answer_total = report["no_answer_total"]

    if no_answer_total:
        print(
            f'No-answer accuracy: '
            f'{report["no_answer_correct"]}/{no_answer_total} '
            f'({report["no_answer_correct"] / no_answer_total * 100:.1f}%)'
        )


def main():
    cards = load_processed_knowledge_cards(
        KNOWLEDGE_PATH
    )

    with open(
        EVAL_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    print(
        f"Loaded {len(cards)} knowledge cards "
        f"and {len(cases)} evaluation cases."
    )

    print()
    print("Keyword Retriever Details")
    print("=" * 60)

    keyword_report = evaluate_keyword(
        cards,
        cases,
    )

    print()
    print("Semantic Retriever Details")
    print("=" * 60)

    semantic_report = evaluate_semantic(
        cards,
        cases,
    )

    print()
    print("Hybrid Retriever Details")
    print("=" * 60)

    hybrid_report = evaluate_hybrid(
        cards,
        cases,
    )

    print_report(
        "Keyword Retriever",
        keyword_report,
    )

    print_report(
        "Semantic Retriever",
        semantic_report,
    )

    print_report(
        "Hybrid Retriever",
        hybrid_report,
    )


if __name__ == "__main__":
    main()


def evaluate_hybrid(cards, cases):
    retriever = HybridRetriever(
        keyword_weight=0.7,
        semantic_weight=0.3,
    )

    print()
    print("Building hybrid index...")
    retriever.build_index(cards)

    hit1 = 0
    hit3 = 0
    no_answer_correct = 0
    no_answer_total = 0
    positive_total = 0

    for case in cases:
        results = retriever.retrieve(
            case["question"],
            top_k=3,
        )

        predicted_names = [
            item["card"].get("name")
            for item in results
        ]

        expected = case["expected_name"]

        if expected is None:
            no_answer_total += 1

            if not results:
                no_answer_correct += 1

            continue

        positive_total += 1

        if predicted_names:
            if predicted_names[0] == expected:
                hit1 += 1

        if expected in predicted_names[:3]:
            hit3 += 1

    return {
        "hit1": hit1,
        "hit3": hit3,
        "positive_total": positive_total,
        "no_answer_correct": no_answer_correct,
        "no_answer_total": no_answer_total,
    }
