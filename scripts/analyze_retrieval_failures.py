import json
from pathlib import Path

from src.hybrid_retriever import HybridRetriever
from src.loader import load_processed_knowledge_cards


KNOWLEDGE_PATH = Path(
    "data/knowledge/processed/knowledge_cards.json"
)

EVALUATION_PATH = Path(
    "data/evaluation_zh.json"
)

REPORT_PATH = Path(
    "reports/retrieval_failure_analysis.json"
)


def get_question(case: dict) -> str:
    question = (
        case.get("question")
        or case.get("query")
        or ""
    )

    return str(
        question
    ).strip()


def get_expected_name(case: dict) -> str:
    expected_name = case.get(
        "expected_name"
    )

    if expected_name is None:
        return ""

    return str(
        expected_name
    ).strip()


def serialize_result(
    result: dict,
    rank: int,
) -> dict:
    card = result.get(
        "card",
        {},
    )

    return {
        "rank": rank,
        "card_id": card.get(
            "id",
            "",
        ),
        "name": card.get(
            "name",
            "",
        ),
        "hybrid_score": round(
            float(
                result.get(
                    "score",
                    0.0,
                )
            ),
            4,
        ),
        "keyword_score": round(
            float(
                result.get(
                    "keyword_score",
                    0.0,
                )
            ),
            4,
        ),
        "semantic_score": round(
            float(
                result.get(
                    "semantic_score",
                    0.0,
                )
            ),
            4,
        ),
    }


def classify_failure(
    expected_name: str,
    results: list[dict],
) -> str:
    if not expected_name:
        if results:
            return "false_positive"

        return "correct_rejection"

    if not results:
        return "no_retrieval"

    names = [
        result.get(
            "card",
            {},
        ).get(
            "name",
            "",
        )
        for result in results
    ]

    if names[0] == expected_name:
        return "success"

    if expected_name in names:
        return "ranking_failure"

    return "recall_failure"


def find_expected_rank(
    expected_name: str,
    results: list[dict],
) -> int | None:
    if not expected_name:
        return None

    for rank, result in enumerate(
        results,
        start=1,
    ):
        name = result.get(
            "card",
            {},
        ).get(
            "name",
            "",
        )

        if name == expected_name:
            return rank

    return None


def main():
    cards = load_processed_knowledge_cards(
        KNOWLEDGE_PATH
    )

    with open(
        EVALUATION_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        evaluation_cases = json.load(
            file
        )

    retriever = HybridRetriever(
        keyword_weight=0.7,
        semantic_weight=0.3,
    )

    retriever.build_index(
        cards
    )

    analyses = []

    counters = {
        "total": 0,
        "success": 0,
        "correct_rejection": 0,
        "ranking_failure": 0,
        "recall_failure": 0,
        "no_retrieval": 0,
        "false_positive": 0,
    }

    print(
        "Structured Retrieval Failure Analysis"
    )

    print(
        "=" * 70
    )

    for index, case in enumerate(
        evaluation_cases,
        start=1,
    ):
        question = get_question(
            case
        )

        expected_name = get_expected_name(
            case
        )

        if not question:
            print(
                f"[SKIP] Case {index}: "
                "missing question"
            )
            continue

        results = retriever.retrieve(
            question,
            top_k=3,
        )

        failure_type = classify_failure(
            expected_name,
            results,
        )

        expected_rank = find_expected_rank(
            expected_name,
            results,
        )

        serialized_results = [
            serialize_result(
                result,
                rank,
            )
            for rank, result in enumerate(
                results,
                start=1,
            )
        ]

        analysis = {
            "case_index": index,
            "question": question,
            "expected_name": expected_name,
            "expected_rank": expected_rank,
            "status": failure_type,
            "top_results": serialized_results,
        }

        analyses.append(
            analysis
        )

        counters["total"] += 1
        counters[failure_type] += 1

        status_label = (
            "PASS"
            if failure_type
            in {
                "success",
                "correct_rejection",
            }
            else "FAIL"
        )

        print()
        print(
            f"[{status_label}] "
            f"Case {index}"
        )

        print(
            f"Question : {question}"
        )

        print(
            "Expected : "
            f"{expected_name or 'NO ANSWER'}"
        )

        print(
            f"Type     : {failure_type}"
        )

        if expected_rank is not None:
            print(
                "Expected Rank: "
                f"{expected_rank}"
            )

        if serialized_results:
            print(
                "Top Results:"
            )

            for item in serialized_results:
                print(
                    "  "
                    f"#{item['rank']} "
                    f"{item['name']} "
                    f"(hybrid="
                    f"{item['hybrid_score']}, "
                    f"keyword="
                    f"{item['keyword_score']}, "
                    f"semantic="
                    f"{item['semantic_score']})"
                )

        else:
            print(
                "Top Results: NONE"
            )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = {
        "summary": counters,
        "cases": analyses,
    }

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print(
        "=" * 70
    )

    print(
        "Summary"
    )

    print(
        "=" * 70
    )

    print(
        f"Total             : "
        f"{counters['total']}"
    )

    print(
        f"Success           : "
        f"{counters['success']}"
    )

    print(
        f"Correct Rejection : "
        f"{counters['correct_rejection']}"
    )

    print(
        f"Ranking Failure   : "
        f"{counters['ranking_failure']}"
    )

    print(
        f"Recall Failure    : "
        f"{counters['recall_failure']}"
    )

    print(
        f"No Retrieval      : "
        f"{counters['no_retrieval']}"
    )

    print(
        f"False Positive    : "
        f"{counters['false_positive']}"
    )

    print()

    print(
        "Report saved to:"
    )

    print(
        REPORT_PATH
    )


if __name__ == "__main__":
    main()
