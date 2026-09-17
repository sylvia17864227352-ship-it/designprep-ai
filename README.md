# DesignPrep AI

DesignPrep AI is a grounded conversational RAG system for design-history learning.

The project started as a lightweight retrieval MVP and was iteratively expanded into a multi-turn AI question-answering product built on a real design-history knowledge base.

## Project Highlights

- 255 real design-history knowledge cards
- Markdown-to-JSON knowledge import pipeline
- Chinese keyword retrieval
- Multilingual semantic retrieval
- Hybrid retrieval and reranking
- Multi-turn query rewriting
- Active-topic tracking for pronoun resolution
- Grounded LLM answer generation
- Source citation and traceability
- Out-of-domain rejection
- Retrieval and answer evaluation
- Bilateral conversational Streamlit UI

---

## 1. Problem

Design-history learning involves many fragmented entities:

- Designers
- Movements
- Schools
- Works
- Concepts
- Historical relationships

Students often need to repeatedly search across textbooks and personal notes.

The product goal is to support a workflow in which users can ask natural-language questions and receive answers grounded in a structured knowledge base.

---

## 2. Final Product Flow

```text
User Question
    ↓
Conversation History
    ↓
Query Rewriter
    ↓
Standalone Query
    ↓
Hybrid Retriever
    ├── Keyword Retrieval
    └── Semantic Retrieval
    ↓
Reranking
    ↓
Top-K Knowledge Cards
    ↓
Context Builder
    ↓
Prompt Builder
    ↓
LLM Provider
    ↓
Grounded Answer
    ↓
Source Citation
```

For multi-turn questions such as:

```text
User:
霍尔塔是谁？

User:
那他的代表作品呢？
```

the query rewriter converts the follow-up into a standalone retrieval query such as:

```text
霍尔塔（维克多·霍塔）的代表作品是什么？
```

before retrieval.

---

## 3. Knowledge Base

The current knowledge base contains:

```text
255 design-history knowledge cards
```

The original cards are stored in Markdown format and converted into structured JSON through an import pipeline.

Each processed card contains fields such as:

```json
{
  "id": "DS-0001",
  "legacy_id": "DS-001",
  "name": "霍尔塔（维克多·霍塔）",
  "knowledge_type": "人物",
  "subject": "设计史论",
  "aliases_keywords": [
    "维克多·霍塔",
    "霍尔塔",
    "比利时线条",
    "鞭线",
    "塔赛旅馆"
  ],
  "questions": [
    "霍尔塔在比利时新艺术运动中的地位和设计特点是什么？",
    "霍尔塔的代表作品是什么？"
  ],
  "standard_answer": "...",
  "memory_points": [],
  "source": {},
  "evidence": "...",
  "review_status": "已审核"
}
```

The system preserves both:

```text
id
→ generated unique internal ID

legacy_id
→ original knowledge-card ID
```

This avoids conflicts in the original numbering while preserving traceability.

---

## 4. Knowledge Import Pipeline

```text
Markdown Knowledge Cards
        ↓
Parser
        ↓
Schema Normalization
        ↓
Unique ID Generation
        ↓
Processed JSON
        ↓
Validation
        ↓
Retrieval System
```

Main import script:

```text
scripts/import_md_cards.py
```

Processed output:

```text
data/knowledge/processed/knowledge_cards.json
```

---

## 5. Retrieval Strategy

Three retrieval strategies were implemented and compared.

### Keyword Retrieval

The keyword retriever uses field-weighted lexical matching.

Example weighting:

```text
name                ×5
aliases / keywords  ×4
common questions    ×3
standard answer     ×2
memory points       ×1
evidence            ×1
```

It also applies a minimum relevance threshold to reject unrelated questions.

### Semantic Retrieval

Semantic retrieval uses:

```text
sentence-transformers
paraphrase-multilingual-MiniLM-L12-v2
```

Knowledge cards and user queries are embedded and compared using cosine similarity.

### Hybrid Retrieval

The final retriever combines:

```text
Keyword relevance
+
Semantic similarity
+
Entity-sensitive ranking
```

This improves Top-1 ranking while preserving semantic recall.

---

## 6. Retrieval Evaluation

The retrieval benchmark contains:

```text
20 Chinese evaluation cases
```

including:

- Direct questions
- Rephrased questions
- Entity questions
- Concept questions
- Negative out-of-domain questions

Current results on this evaluation set:

| Retriever | Hit@1 | Hit@3 | No-answer Accuracy |
|---|---:|---:|---:|
| Keyword | 94.7% | 100.0% | 100.0% |
| Semantic | 63.2% | 100.0% | 100.0% |
| Hybrid | 100.0% | 100.0% | 100.0% |

These results apply only to the current evaluation dataset and should not be interpreted as production-level accuracy.

The comparison showed that semantic retrieval provided strong recall but weaker Top-1 ranking, while the hybrid strategy retained semantic recall and improved ranking precision.

Run the comparison with:

```bash
python -m scripts.compare_retrievers
```

---

## 7. Multi-turn Query Rewriting

The product supports follow-up questions that depend on previous context.

Example:

```text
User:
勒·柯布西耶是谁？

User:
他的理念是什么？
```

The system tracks the active knowledge topic and rewrites the follow-up into a standalone query.

The architecture is:

```text
Conversation History
        ↓
Active Topic
        ↓
Query Rewriter
        ↓
Standalone Query
        ↓
Hybrid Retriever
```

The rewritten retrieval query can also be inspected in the UI for debugging and evaluation.

---

## 8. Grounded RAG Generation

The generation layer is separated from retrieval.

```text
Hybrid Retriever
    ↓
Context Builder
    ↓
Prompt Builder
    ↓
LLM Provider
    ↓
Grounded Answer
```

The LLM is instructed to answer only from retrieved knowledge context.

If retrieval does not return sufficiently relevant evidence, the system responds:

```text
当前知识库中没有足够信息确认。
```

instead of forcing an answer.

---

## 9. Answer Grounding Evaluation

The system includes a separate answer-level evaluation set.

Current grounding benchmark:

```text
6 cases
```

Current result:

```text
6 / 6 passed
100.0%
```

The evaluation checks whether final generated answers contain the expected knowledge points and whether out-of-domain questions are correctly rejected.

This result applies only to the current six-case grounding evaluation set.

Run:

```bash
python -m scripts.evaluate_answer_grounding
```

---

## 10. Conversational Interface

The Streamlit interface supports:

- Bilateral chat layout
- Multi-turn conversation
- Persistent session history
- Grounded AI responses
- Source inspection
- Query-rewrite inspection
- Knowledge-base rejection
- Current knowledge-card count

Run:

```bash
python -m streamlit run src/app.py
```

---

## 11. Project Structure

```text
designprep-ai/
├── data/
│   ├── evaluation_zh.json
│   ├── evaluation_query_rewrite.json
│   ├── evaluation_answer_grounding.json
│   └── knowledge/
│       └── processed/
│           └── knowledge_cards.json
├── docs/
│   ├── architecture.md
│   └── product_scope.md
├── scripts/
│   ├── import_md_cards.py
│   ├── test_processed_retrieval.py
│   ├── test_semantic_retrieval.py
│   ├── test_hybrid_retrieval.py
│   ├── compare_retrievers.py
│   ├── evaluate_query_rewriter.py
│   ├── evaluate_answer_grounding.py
│   └── test_rag_pipeline.py
├── src/
│   ├── loader.py
│   ├── retriever.py
│   ├── semantic_retriever.py
│   ├── hybrid_retriever.py
│   ├── context_builder.py
│   ├── prompt_builder.py
│   ├── query_rewriter.py
│   ├── llm_provider.py
│   ├── rag_pipeline.py
│   └── app.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 12. Installation

Clone the repository:

```bash
git clone <repository-url>
cd designprep-ai
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create:

```text
.env
```

based on:

```text
.env.example
```

Required variables:

```text
LLM_MODEL=
LLM_BASE_URL=
LLM_API_KEY=
```

Never commit the real `.env` file.

---

## 13. Run Tests

Run all automated tests:

```bash
python -m pytest -v
```

Run retrieval comparison:

```bash
python -m scripts.compare_retrievers
```

Run query-rewrite evaluation:

```bash
python -m scripts.evaluate_query_rewriter
```

Run answer-grounding evaluation:

```bash
python -m scripts.evaluate_answer_grounding
```

---

## 14. Development Milestones

### Milestone 1 — Knowledge Foundation & MVP

- Repository initialization
- Product scope
- Technical architecture
- Knowledge-card data model
- Loader
- Basic retrieval
- Answer Builder
- Initial Streamlit MVP
- Automated tests

### Milestone 2 — Knowledge Expansion & Retrieval Evaluation

- 255 real knowledge cards
- Markdown import pipeline
- Processed knowledge schema
- Chinese keyword retrieval
- Semantic retrieval
- Hybrid retrieval
- Retrieval benchmark
- Hit@1 / Hit@3 / rejection evaluation

### Milestone 3 — Grounded Conversational RAG Product

- Context Builder
- Prompt layer
- LLM Provider
- End-to-end RAG pipeline
- Source citation
- Bilateral conversational UI
- Query rewriting
- Active-topic tracking
- Multi-turn follow-up support
- Out-of-domain rejection
- Answer grounding evaluation

---

## 15. Current Limitations

The current product still has several limitations:

- The knowledge base contains only a limited portion of design-history content
- Evaluation datasets remain relatively small
- Duplicate or overlapping source knowledge may still require further consolidation
- Retrieval thresholds are tuned on the current dataset
- Query rewriting depends on an external LLM
- Answer grounding evaluation currently uses a limited rule-based benchmark
- No production deployment or monitoring layer has been implemented

---

## 16. Future Improvements

Potential next steps:

- Expand knowledge coverage
- Add knowledge-card review workflow
- Increase retrieval benchmark size
- Add more difficult adversarial negative cases
- Evaluate query rewriting on a larger multi-turn dataset
- Add LLM-as-a-Judge grounding evaluation
- Add latency and token-cost monitoring
- Cache semantic embeddings
- Add feedback collection
- Add retrieval failure analysis dashboard

---

## 17. Product Development Logic

The project was not implemented as a single generated application.

The development process followed an incremental workflow:

```text
MVP
↓
Real Knowledge Base
↓
Retrieval Baseline
↓
Semantic Retrieval
↓
Benchmark Comparison
↓
Hybrid Retrieval
↓
Grounded RAG
↓
Multi-turn Conversation
↓
Evaluation
```

Each major capability was implemented, tested, evaluated, and recorded through Git commits before the next stage was introduced.