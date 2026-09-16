# Technical Architecture

## 1. System Overview

DesignPrep AI is a lightweight retrieval-based question-answering system for design history learning.

The MVP follows the pipeline:

User Question
→ Question Processing
→ Knowledge Retrieval
→ Relevant Knowledge Cards
→ Answer Construction
→ Answer + Sources

The first runnable version will prioritize deterministic retrieval and source tracing before introducing optional LLM-based answer generation.

## 2. Core Modules

### 2.1 Knowledge Data

Stores structured design-history knowledge cards.

Each knowledge card should contain at least:

- id
- title
- content
- keywords
- category
- source

Example:

    {
      "id": "DS-001",
      "title": "Bauhaus",
      "content": "The Bauhaus was founded by Walter Gropius in 1919...",
      "keywords": ["Bauhaus", "Walter Gropius", "modernism"],
      "category": "design_movement",
      "source": "Design History Notes"
    }

For the MVP, knowledge cards will be stored locally as JSON files.

### 2.2 Knowledge Loader

Responsibilities:

- Read local knowledge-card files
- Validate required fields
- Convert knowledge cards into an internal Python data structure
- Handle missing or malformed data

Planned module:

    src/loader.py

### 2.3 Retriever

Responsibilities:

- Receive a user question
- Compare the question with available knowledge cards
- Rank potentially relevant cards
- Return Top-K retrieval results

The first version will use lightweight keyword-based retrieval.

More advanced semantic retrieval can be added later if necessary.

Planned module:

    src/retriever.py

### 2.4 Answer Builder

Responsibilities:

- Receive the user question and retrieved knowledge cards
- Construct a concise answer from retrieved information
- Preserve source references
- Return a fallback response when no reliable knowledge is retrieved

The initial version will not require an external LLM.

An LLM-based generation layer may be introduced as a later enhancement after the retrieval pipeline is validated.

Planned module:

    src/answer.py

### 2.5 User Interface

The MVP interface will be implemented with Streamlit.

The interface should allow users to:

- Enter a natural-language question
- Submit the question
- View the generated answer
- View retrieved knowledge cards
- View source information
- See a clear message when no relevant knowledge is found

Planned module:

    src/app.py

### 2.6 Evaluation

A small evaluation dataset will be created to test retrieval quality.

Each test case should contain:

- question
- expected knowledge-card ID
- expected key information

The evaluation layer will initially measure:

- whether the expected card appears in Top-K results
- retrieval success rate
- failed retrieval cases

Planned files:

    data/evaluation.json
    tests/test_retriever.py

## 3. Initial Technical Stack

- Python 3.x
- JSON for structured knowledge-card storage
- Streamlit for the user interface
- Pytest for automated testing
- Standard Python libraries for the initial retrieval implementation

Optional later dependencies may include:

- sentence-transformers for semantic retrieval
- FAISS or another vector index
- an LLM API for answer generation

These are outside the initial MVP unless the basic retrieval pipeline is stable.

## 4. Planned Project Structure

    designprep-ai/
    ├── data/
    │   ├── knowledge/
    │   │   └── sample_cards.json
    │   └── evaluation.json
    ├── docs/
    │   ├── product_scope.md
    │   └── architecture.md
    ├── src/
    │   ├── __init__.py
    │   ├── loader.py
    │   ├── retriever.py
    │   ├── answer.py
    │   └── app.py
    ├── tests/
    │   ├── test_loader.py
    │   └── test_retriever.py
    ├── .gitignore
    ├── README.md
    └── requirements.txt

## 5. Module Data Flow

The expected internal flow is:

    question: str
        ↓
    retriever.retrieve(question)
        ↓
    List[KnowledgeCard]
        ↓
    answer.build_answer(question, cards)
        ↓
    {
        "answer": "...",
        "sources": [...],
        "retrieved_cards": [...]
    }

This interface may evolve during implementation, but module responsibilities should remain separated.

## 6. Error Handling

The MVP should handle at least the following cases:

- Empty user question
- Missing knowledge file
- Invalid knowledge-card format
- No relevant retrieval result
- Duplicate knowledge-card IDs

Errors should produce understandable messages rather than application crashes.

## 7. Testing Strategy

Testing will be introduced incrementally.

The MVP should include:

- Knowledge-loader tests
- Retrieval tests
- Empty-query tests
- Invalid-data tests
- Evaluation against a small question set

Each major module should be testable independently before integration.

## 8. Development Principles

The project will be developed incrementally.

Each milestone should:

1. Introduce one clearly defined capability
2. Produce a runnable or testable state
3. Be verified before moving to the next stage
4. Be recorded through meaningful Git commits

The repository should reflect the actual development process rather than a completed project being divided retrospectively.

## 9. Planned Milestones

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
- Loader tests

### Milestone 3 — Retrieval Pipeline

Deliverables:

- Keyword-based retrieval
- Top-K ranking
- Retrieval tests
- Initial evaluation dataset

### Milestone 4 — Question-Answering Application

Deliverables:

- Answer builder
- Source tracing
- Streamlit interface
- End-to-end runnable workflow

### Milestone 5 — Evaluation and Refinement

Deliverables:

- Expanded evaluation dataset
- Retrieval-quality analysis
- Error handling
- Documentation improvements
- Final runnable MVP

## 10. MVP Boundary

The MVP focuses on proving the complete workflow:

Question
→ Retrieval
→ Answer
→ Source
→ Evaluation

The project does not initially aim to build a production-scale RAG system or train a language model.