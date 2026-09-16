from pathlib import Path
import json
import re


RAW_DIR = Path("data/knowledge/raw")
OUTPUT_FILE = Path(
    "data/knowledge/processed/knowledge_cards.json"
)


def extract_section(
    text: str,
    heading: str,
    next_headings: list[str],
) -> str:
    start_pattern = (
        re.escape(heading)
        + r"\s*[:：]?\s*"
    )

    start_match = re.search(
        start_pattern,
        text,
    )

    if not start_match:
        return ""

    start = start_match.end()
    end = len(text)

    for next_heading in next_headings:
        next_match = re.search(
            re.escape(next_heading)
            + r"\s*[:：]?",
            text[start:],
        )

        if next_match:
            candidate_end = (
                start
                + next_match.start()
            )

            end = min(
                end,
                candidate_end,
            )

    return text[start:end].strip()


def parse_list_block(
    block: str,
) -> list[str]:
    items = []

    for line in block.splitlines():
        line = line.strip()

        if not line:
            continue

        line = re.sub(
            r"^\d+[\.、]\s*",
            "",
            line,
        )

        if line:
            items.append(line)

    return items


def parse_keywords(
    block: str,
) -> list[str]:
    if not block:
        return []

    parts = re.split(
        r"[；;，,\n]+",
        block,
    )

    return [
        item.strip()
        for item in parts
        if item.strip()
    ]


def parse_source(
    block: str,
) -> dict:
    parts = [
        item.strip()
        for item in re.split(
            r"[；;]",
            block,
        )
        if item.strip()
    ]

    source = {
        "source_id": None,
        "file": None,
        "chapter": None,
        "page": None,
        "book": None,
    }

    if len(parts) > 0:
        source["source_id"] = parts[0]

    if len(parts) > 1:
        source["file"] = parts[1]

    if len(parts) > 2:
        source["chapter"] = parts[2]

    if len(parts) > 3:
        page_match = re.search(
            r"(\d+)",
            parts[3],
        )

        if page_match:
            source["page"] = int(
                page_match.group(1)
            )

    if len(parts) > 4:
        source["book"] = parts[4]

    return source


def parse_card(
    file_path: Path,
    generated_id: str,
) -> dict:
    text = file_path.read_text(
        encoding="utf-8"
    )

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    legacy_id = (
        lines[0]
        if lines
        else ""
    )

    name_match = re.search(
        r"知识点名称[:：]\s*(.+)",
        text,
    )

    type_match = re.search(
        r"知识类型[:：]\s*(.+)",
        text,
    )

    subject_match = re.search(
        r"所属科目[:：]\s*(.+)",
        text,
    )

    chapter_match = re.search(
        r"所属章节[:：]\s*(.+)",
        text,
    )

    status_match = re.search(
        r"审核状态[:：]?\s*(.+)",
        text,
    )

    keywords_block = extract_section(
        text,
        "别名与关键词",
        [
            "常见问题",
            "标准答案",
        ],
    )

    questions_block = extract_section(
        text,
        "常见问题",
        [
            "标准答案",
        ],
    )

    answer_block = extract_section(
        text,
        "标准答案",
        [
            "核心记忆点",
        ],
    )

    memory_block = extract_section(
        text,
        "核心记忆点",
        [
            "易混淆点",
        ],
    )

    confusion_block = extract_section(
        text,
        "易混淆点",
        [
            "资料来源",
        ],
    )

    source_block = extract_section(
        text,
        "资料来源",
        [
            "证据原文",
        ],
    )

    evidence_block = extract_section(
        text,
        "证据原文",
        [
            "审核状态",
        ],
    )

    return {
        "id": generated_id,
        "legacy_id": legacy_id,
        "name": (
            name_match.group(1).strip()
            if name_match
            else ""
        ),
        "knowledge_type": (
            type_match.group(1).strip()
            if type_match
            else ""
        ),
        "subject": (
            subject_match.group(1).strip()
            if subject_match
            else ""
        ),
        "chapter": (
            chapter_match.group(1).strip()
            if chapter_match
            else ""
        ),
        "aliases_keywords": (
            parse_keywords(
                keywords_block
            )
        ),
        "questions": (
            parse_list_block(
                questions_block
            )
        ),
        "standard_answer": (
            answer_block
        ),
        "memory_points": (
            parse_list_block(
                memory_block
            )
        ),
        "confusions": (
            []
            if confusion_block
            in {"", "待补充"}
            else parse_list_block(
                confusion_block
            )
        ),
        "source": (
            parse_source(
                source_block
            )
        ),
        "evidence": (
            evidence_block
        ),
        "review_status": (
            status_match.group(1).strip()
            if status_match
            else ""
        ),
        "source_file": file_path.name,
    }


def main():
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    md_files = sorted(
        RAW_DIR.glob("*.md")
    )

    cards = []

    for index, file_path in enumerate(
        md_files,
        start=1,
    ):
        generated_id = (
            f"DS-{index:04d}"
        )

        card = parse_card(
            file_path,
            generated_id,
        )

        cards.append(card)

    OUTPUT_FILE.write_text(
        json.dumps(
            cards,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Imported {len(cards)} "
        "knowledge cards."
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print()

    if cards:
        print(
            "First generated ID:",
            cards[0]["id"],
        )

        print(
            "Last generated ID:",
            cards[-1]["id"],
        )


if __name__ == "__main__":
    main()
