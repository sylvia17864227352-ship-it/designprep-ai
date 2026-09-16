# DesignPrep AI

DesignPrep AI is a lightweight design-history question-answering system built to demonstrate a complete retrieval-based AI product workflow.

The current MVP supports:

- Local structured knowledge cards
- Keyword-based retrieval
- Answer construction from retrieved evidence
- Source tracing
- Basic irrelevant-query rejection
- Automated tests
- Retrieval evaluation
- Streamlit web interface

---

## 1. Product Goal

Design history contains many fragmented concepts, designers, movements, schools, works, and chronological relationships.

Students preparing for industrial design postgraduate entrance examinations often need to search repeatedly across textbooks, notes, and personal knowledge bases.

DesignPrep AI aims to provide a lightweight workflow in which users can ask a natural-language question and receive:

- A directly relevant knowledge answer
- The matched knowledge card
- Source information
- Retrieval details

The current MVP focuses on validating the complete retrieval-based question-answering workflow rather than building a production-scale AI system.

---

## 2. Current Workflow

```text
User Question
    ↓
Question Processing
    ↓
Knowledge Retrieval
    ↓
Top-K Knowledge Cards
    ↓
Answer Builder
    ↓
Answer + Source + Retrieval Details
```

The current MVP uses deterministic retrieval and does not require an external LLM.

This allows retrieval quality, source tracing, and failure cases to be evaluated independently before adding generative capabilities.

---

## 3. Project Structure

```text
designprep-ai/
├── data/
│   ├── evaluation.json
│   └── knowledge/
│       └── sample_cards.json
├── docs/
│   ├── architecture.md
│   └── product_scope.md
├── src/
│   ├── __init__.py
│   ├── loader.py
│   ├── retriever.py
│   ├── answer.py
│   ├── evaluate.py
│   └── app.py
├── tests/
│   ├── test_loader.py
│   ├── test_retriever.py
│   └── test_answer.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 4. Knowledge Card Format

The knowledge base is currently stored as structured JSON knowledge cards.

Example:

```json
{
  "id": "DS-001",
  "title": "Bauhaus",
  "content": "The Bauhaus was founded by Walter Gropius in Weimar in 1919. It aimed to unify art, craft, and technology and became one of the most influential schools of modern design.",
  "keywords": [
    "Bauhaus",
    "Walter Gropius",
    "modern design",
    "Weimar"
  ],
  "category": "design_movement",
  "source": "Design History Notes"
}
```

Each card contains:

- `id`: unique knowledge-card identifier
- `title`: main topic
- `content`: core knowledge content
- `keywords`: retrieval keywords
- `category`: knowledge category
- `source`: original source information

---

## 5. Knowledge Loading and Validation

The knowledge loader is implemented in:

```text
src/loader.py
```

It is responsible for:

- Loading JSON knowledge cards
- Checking whether the data file exists
- Validating required fields
- Validating the keyword structure
- Detecting duplicate knowledge-card IDs
- Returning structured Python objects for later retrieval

Invalid or malformed data raises explicit errors rather than silently entering the retrieval pipeline.

---

## 6. Retrieval Strategy

The current retriever uses a lightweight weighted keyword-matching strategy.

The implementation is located in:

```text
src/retriever.py
```

The current relevance weights are:

- Title match: ×3
- Keyword match: ×2
- Content match: ×1

For example:

```text
Question:
Who founded the Bauhaus?

Retrieved card:
DS-001 — Bauhaus
```

The retriever ranks cards according to their relevance score and returns the Top-K results.

A minimum relevance threshold is also applied.

This prevents the system from forcing an unrelated answer when no sufficiently relevant knowledge is available.

For example:

```text
Question:
Who designed the iPhone?
```

The current design-history knowledge base does not contain a relevant answer, so the system should return no relevant retrieval result instead of incorrectly selecting the closest available card.

---

## 7. Answer Builder

The Answer Builder is implemented in:

```text
src/answer.py
```

Its current responsibilities are:

- Receive the user question
- Receive ranked retrieval results
- Select the strongest retrieved evidence
- Construct the answer from the retrieved knowledge card
- Return source information
- Preserve retrieval details
- Return a fallback response when no relevant evidence is found

The current version does not use an external LLM.

This means answers remain directly grounded in stored knowledge-card content.

The basic pipeline is:

```text
Question
    ↓
Retriever
    ↓
Relevant Knowledge Card
    ↓
Answer Builder
    ↓
Answer + Source
```

---

## 8. User Interface

The MVP interface is implemented with Streamlit:

```text
src/app.py
```

The interface supports:

- Natural-language question input
- Example questions
- Answer display
- Source display
- Knowledge-card ID display
- Retrieval-score inspection
- Empty-query warning
- No-relevant-result fallback
- Knowledge-loading error handling

The interface is intended to expose the full retrieval workflow rather than hide retrieval behavior behind a black-box answer.

---

## 9. Installation

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd designprep-ai
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Current dependencies include:

```text
pytest
streamlit
```

---

## 10. Run the Application

Start the Streamlit application:

```bash
python -m streamlit run src/app.py
```

The terminal will display a local URL, typically similar to:

```text
http://localhost:8501
```

Open the URL in a browser.

Example questions:

```text
Who founded the Bauhaus?

What did William Morris criticize?

Which school emphasized systematic design methods?
```

An irrelevant question can also be used to test fallback behavior:

```text
Who designed the iPhone?
```

---

## 11. Automated Testing

The project uses Pytest for automated testing.

Run the complete test suite:

```bash
python -m pytest -v
```

The current tests cover:

### Knowledge Loader

- Successful knowledge-card loading
- Missing-file handling
- Missing required fields
- Duplicate knowledge-card IDs

### Retriever

- Correct Bauhaus retrieval
- Correct Arts and Crafts retrieval
- Correct Ulm retrieval
- Empty-query handling
- Irrelevant-query rejection

### Answer Builder

- Answer construction
- Source tracing
- Empty-question handling
- No-result fallback

The purpose of these tests is to verify software behavior and prevent later changes from breaking existing functionality.

---

## 12. Evaluation Dataset

In addition to software tests, the repository includes a manually constructed retrieval evaluation set:

```text
data/evaluation.json
```

Each evaluation case contains:

```json
{
  "id": "EVAL-001",
  "question": "Who founded the Bauhaus?",
  "expected_card_id": "DS-001",
  "expected_keywords": [
    "Walter Gropius",
    "1919"
  ]
}
```

The `expected_card_id` serves as manually defined ground truth.

The evaluation set contains both:

- Positive retrieval cases
- Negative no-answer cases

For a negative case:

```json
{
  "id": "EVAL-006",
  "question": "Who designed the iPhone?",
  "expected_card_id": null,
  "expected_keywords": []
}
```

This allows the system to evaluate not only whether it can retrieve relevant knowledge, but also whether it can correctly avoid answering when no suitable knowledge exists.

---

## 13. Run Retrieval Evaluation

The evaluation pipeline is implemented in:

```text
src/evaluate.py
```

Run:

```bash
python -m src.evaluate
```

The evaluation script:

```text
Loads evaluation cases
        ↓
Runs each question through the retriever
        ↓
Obtains the predicted Top-1 card
        ↓
Compares prediction with expected_card_id
        ↓
Calculates Top-1 Accuracy
```

Example output:

```text
Evaluation Results
------------------
EVAL-001 PASS (expected=DS-001, predicted=DS-001)
EVAL-002 PASS (expected=DS-002, predicted=DS-002)
EVAL-003 PASS (expected=DS-003, predicted=DS-003)
EVAL-004 PASS (expected=DS-001, predicted=DS-001)
EVAL-005 PASS (expected=DS-002, predicted=DS-002)
EVAL-006 PASS (expected=None, predicted=None)

Top-1 Accuracy: 100.0%
6 / 6 correct
```

---

## 14. Current Evaluation Result

Current evaluation set size:

```text
6 cases
```

Current metric:

```text
Top-1 Accuracy
```

If the latest local evaluation produces:

```text
6 / 6 correct
Top-1 Accuracy: 100.0%
```

the result can be summarized as:

> Top-1 Accuracy: 100.0% on the current six-case evaluation set.

This result should be interpreted carefully.

The current evaluation dataset is intentionally small and is used to validate the MVP workflow.

It should not be interpreted as evidence of production-level retrieval accuracy.

---

## 15. Tests vs Evaluation

Automated tests and retrieval evaluation serve different purposes.

### Automated Tests

Pytest verifies whether software behavior remains correct.

For example:

```text
Does the loader reject duplicate IDs?

Does an empty question return an empty retrieval result?

Does the Answer Builder return source information?
```

### Evaluation

The evaluation dataset measures whether the product capability performs correctly on predefined knowledge questions.

For example:

```text
Question:
Who founded the Bauhaus?

Expected:
DS-001

Predicted:
DS-001
```

This distinction allows engineering correctness and retrieval quality to be assessed separately.

---

## 16. Current MVP Boundary

The current MVP demonstrates:

```text
Structured Knowledge
        ↓
Knowledge Loading
        ↓
Retrieval
        ↓
Answer Construction
        ↓
Source Tracing
        ↓
Evaluation
        ↓
User Interface
```

The project intentionally does not attempt to implement a production-scale RAG system at this stage.

Current out-of-scope capabilities include:

- User accounts
- Cloud deployment
- Payment
- Large-scale vector databases
- Model fine-tuning
- User-uploaded textbooks
- Large-scale semantic retrieval
- Production monitoring infrastructure

---

## 17. Current Limitations

The current version has several important limitations.

### Small Knowledge Base

Only a small set of sample knowledge cards is currently included.

### Lexical Retrieval

The retriever relies primarily on word overlap rather than semantic similarity.

Questions using very different wording may therefore fail even when relevant knowledge exists.

### Limited Chinese Support

The initial tokenizer was designed primarily around English text.

Chinese tokenization and Chinese retrieval quality still require further improvement.

### Small Evaluation Dataset

The current evaluation set contains only a small number of manually constructed cases.

The current accuracy result therefore represents only the current MVP test scope.

### Deterministic Answer Construction

The Answer Builder currently returns information directly from retrieved knowledge cards instead of generating a more natural response using a language model.

---

## 18. Planned Improvements

Potential next steps include:

### Knowledge Base Expansion

Replace sample cards with a larger set of real design-history knowledge cards.

### Chinese Retrieval

Improve Chinese tokenization and support Chinese design-history questions.

### Knowledge Import Pipeline

Support:

```text
Textbook / OCR
    ↓
Knowledge Extraction
    ↓
Structured Knowledge Cards
    ↓
Human Review
    ↓
Knowledge Base
```

### Semantic Retrieval

Compare the current keyword retriever with semantic embedding retrieval.

Potential future options include:

- sentence-transformers
- vector embeddings
- FAISS
- hybrid keyword + semantic retrieval

### Expanded Evaluation

Increase evaluation coverage across:

- Designers
- Design movements
- Design schools
- Historical periods
- Works
- Concepts
- Similar or ambiguous questions
- Negative questions

### LLM-Based Answer Generation

After retrieval quality is validated, an LLM layer can be introduced:

```text
Question
    ↓
Retriever
    ↓
Top-K Knowledge Cards
    ↓
LLM with retrieved context
    ↓
Grounded Answer
    ↓
Source
```

The retrieval layer should remain independently evaluable even after adding an LLM.

---

## 19. Development Approach

The project was implemented incrementally rather than generated as a completed application in one step.

Development stages included:

1. Repository initialization
2. Product-scope definition
3. Technical-architecture definition
4. Knowledge-card data model
5. Knowledge loader
6. Loader validation tests
7. Keyword retrieval
8. Retriever tests
9. Retrieval evaluation dataset
10. Evaluation pipeline
11. Answer Builder
12. Source tracing
13. Streamlit interface
14. UI-state handling
15. Irrelevant-query rejection
16. Evaluation expansion
17. Documentation refinement

Each stage was run and verified before moving to the next capability.

---

## 20. Development Milestones

### Milestone 1 — Repository and Product Definition

Deliverables:

- Repository initialization
- README
- Product scope
- Technical architecture

### Milestone 2 — Knowledge Data Layer

Deliverables:

- Knowledge-card schema
- Sample knowledge cards
- Knowledge loader
- Data validation
- Loader tests

### Milestone 3 — Retrieval and Evaluation

Deliverables:

- Keyword-based retriever
- Weighted relevance scoring
- Top-K retrieval
- Retrieval tests
- Evaluation dataset
- Top-1 Accuracy evaluation
- Irrelevant-query rejection

### Milestone 4 — Question-Answering MVP

Deliverables:

- Answer Builder
- Source tracing
- Streamlit interface
- Retrieval-detail display
- Empty-query handling
- No-answer fallback

### Milestone 5 — Evaluation and Refinement

Deliverables:

- Expanded evaluation cases
- Negative-query evaluation
- Full regression testing
- README and usage documentation
- Final MVP validation

---

## 21. Current MVP Status

At the current stage, the MVP supports the complete workflow:

```text
Question
    ↓
Retrieval
    ↓
Relevant Knowledge
    ↓
Answer
    ↓
Source
    ↓
Evaluation
```

The system can be run locally, tested automatically, and evaluated against manually labeled retrieval cases.

The next major development direction is to replace the small sample dataset with a larger real design-history knowledge base and improve Chinese-language retrieval.