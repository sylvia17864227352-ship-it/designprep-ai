import json

from src.llm_provider import LLMProvider
from src.query_rewriter import QueryRewriter


EVAL_PATH = "data/evaluation_query_rewrite.json"


def main():
    with open(
        EVAL_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    llm = LLMProvider()

    rewriter = QueryRewriter(
        llm=llm,
    )

    passed = 0

    print("Query Rewrite Evaluation")
    print("=" * 60)

    for case in cases:
        rewritten = rewriter.rewrite(
            case["question"],
            case["history"],
        )

        expected_keywords = case[
            "expected_keywords"
        ]

        is_passed = all(
            keyword in rewritten
            for keyword in expected_keywords
        )

        if is_passed:
            passed += 1

        print()
        print(case["id"])
        print("Original :", case["question"])
        print("Rewritten:", rewritten)
        print(
            "Result   :",
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
