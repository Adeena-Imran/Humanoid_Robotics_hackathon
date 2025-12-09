# RAG Chatbot Implementation Tasks

**Branch**: `005-rag-chatbot` | **Date**: 2025-12-09 | **Plan**: [specs/005-rag-chatbot/plan.md](specs/005-rag-chatbot/plan.md)
**Feature Spec**: [specs/005-rag-chatbot/spec.md](specs/005-rag-chatbot/spec.md)

## Summary

This document outlines the actionable tasks for implementing the RAG Chatbot feature, organized into phases based on dependencies and user stories. The goal is to build a FastAPI-based RAG service that integrates with Qdrant for vector search, Neon Postgres for metadata, and an existing Docusaurus frontend.

## Dependencies

*   **User Story Completion Order:**
    *   Phase 1 (Setup)
    *   Phase 2 (Foundational RAG Components)
    *   US5: Query Outside Book Content (Guardrail)
    *   US3: Topic-Based Explanation
    *   US2: Selected Text Explanation
    *   US1: Chapter Summary Request
    *   US4: Whole-Book Summary Request
    *   Phase 4 (Integration & Polish)

## Parallel Execution Opportunities

*   Many tasks within a given user story can be executed in parallel (marked with [P]).
*   Frontend integration (US6) can begin once the FastAPI service API is stable (after US5/US3/US2/US1/US4 core logic is done).

## Implementation Strategy

*   **MVP First:** Focus on getting a functional RAG pipeline with basic explanation (US3) and refusal (US5) working first.
*   **Incremental Delivery:** Build out each user story sequentially, ensuring each is independently testable before moving to the next.
*   **Test-Driven Development (TDD):** While specific test tasks are not explicitly requested here, TDD is recommended for critical components (e.g., chunking, embedding, retrieval logic, FastAPI endpoint handlers).

---

## Phase 1: Setup (RAG Service Project Initialization)

**Goal**: Establish the basic project structure and environment for the FastAPI RAG service.

-   [ ] T001 Create top-level `rag-service/` directory and `README.md` file.
-   [ ] T002 Initialize Python virtual environment in `rag-service/.venv`.
-   [ ] T003 Create `rag-service/requirements.txt` with core dependencies (FastAPI, Uvicorn, Pytest, python-dotenv, qdrant-client, psycopg2-binary, openai, tiktoken).
-   [ ] T004 Install dependencies from `rag-service/requirements.txt`.
-   [ ] T005 Create basic FastAPI application structure in `rag-service/src/main.py`.
-   [ ] T006 Implement basic FastAPI app instance and run command in `rag-service/app.py`.
-   [ ] T007 Configure `.env` file for API keys and database connections in `rag-service/.env`.
-   [ ] T008 Create `rag-service/tests/conftest.py` for `pytest` fixtures.

---

## Phase 2: Foundational RAG Components (Core Infrastructure)

**Goal**: Implement the core data ingestion pipeline, database clients, and LLM setup.

-   [ ] T009 Create `rag-service/src/config.py` for loading environment variables and configuration.
-   [ ] T010 Create `rag-service/src/db/qdrant.py` for Qdrant client initialization and connection management.
-   [ ] T011 Create `rag-service/src/db/postgres.py` for Neon Serverless Postgres client initialization and connection management.
-   [ ] T012 Develop `rag-service/src/ingestion/schema.py` for defining `ContentChunk` and `ChapterSummary` Pydantic models.
-   [ ] T013 Implement `rag-service/src/ingestion/chunker.py` with hierarchical chunking logic (chapter -> section -> paragraph).
-   [ ] T014 Implement `rag-service/src/ingestion/metadata_extractor.py` for extracting metadata from Markdown/MDX files.
-   [ ] T015 Implement `rag-service/src/ingestion/embedder.py` for generating embeddings using an LLM client.
-   [ ] T016 Implement `rag-service/src/ingestion/pipeline.py` to orchestrate reading, chunking, metadata extraction, embedding, and storing.
-   [ ] T017 (P) Implement `rag-service/src/ingestion/qdrant_manager.py` for creating and managing Qdrant collections.
-   [ ] T018 (P) Implement `rag-service/src/ingestion/postgres_manager.py` for creating and managing Postgres tables for metadata.
-   [ ] T019 Develop `rag-service/scripts/ingest_data.py` CLI script to run the full ingestion pipeline from `my-textbook-site/docs/`.
-   [ ] T020 Run `rag-service/scripts/ingest_data.py` to populate initial Qdrant and Neon Postgres with book content.
-   [ ] T021 Implement `rag-service/src/llm/client.py` for LLM client initialization and basic text generation.
-   [ ] T022 Develop `rag-service/src/llm/prompts.py` for base prompt templates (explanation, summary).

---

## Phase 3: User Story Implementation

### US5: Query Outside Book Content (Guardrail) [P1]

**Goal**: Ensure the chatbot correctly identifies and refuses queries outside the scope of the book.

**Independent Test Criteria**: A query clearly outside the book's content results in the exact refusal message: "This topic is not covered in the book."

-   [ ] T023 [US5] Implement `rag-service/src/services/refusal_service.py` to check if a query is within the book's domain (e.g., using a general LLM check or semantic similarity to overall book embeddings).
-   [ ] T024 [P] [US5] Add endpoint `POST /chat` to `rag-service/src/main.py` for handling chat requests, integrating `refusal_service`.
-   [ ] T025 [US5] Implement logic in `rag-service/src/main.py` to return the specific refusal message when `refusal_service` indicates an out-of-scope query.

### US3: Topic-Based Explanation [P1]

**Goal**: Provide accurate explanations for topics covered in the book using semantic search.

**Independent Test Criteria**: A query for a known topic in the book returns a relevant, accurate explanation sourced from the book content.

-   [ ] T026 [US3] Implement `rag-service/src/retrieval/semantic_search.py` for querying Qdrant with user query embeddings.
-   [ ] T027 [US3] Implement `rag-service/src/services/explanation_service.py` to orchestrate semantic search, context gathering, and LLM prompting for topic explanations.
-   [ ] T028 [P] [US3] Update `POST /chat` endpoint in `rag-service/src/main.py` to handle `query_type: 'explanation'` for topic explanations, integrating `explanation_service`.
-   [ ] T029 [P] [US3] Refine `rag-service/src/llm/prompts.py` with a specific prompt for topic-based explanations.

### US2: Selected Text Explanation [P1]

**Goal**: Provide explanations for selected text, strictly adhering to its boundaries.

**Independent Test Criteria**: A query with selected text returns an explanation based *only* on that text, even if it's incomplete.

-   [ ] T030 [US2] Update `rag-service/src/services/explanation_service.py` to handle `selected_text` from the request.
-   [ ] T031 [US2] Refine LLM prompting in `rag-service/src/llm/prompts.py` to strictly enforce "selected text only" constraint.
-   [ ] T032 [P] [US2] Update `POST /chat` endpoint in `rag-service/src/main.py` to correctly parse `selected_text` and route to `explanation_service`.

### US1: Chapter Summary Request [P1]

**Goal**: Generate concise summaries for specific chapters, handling embedded questions gracefully.

**Independent Test Criteria**: A request for a chapter summary returns an accurate summary. If an embedded question is detected, the summary is returned, followed by a prompt to ask the question separately.

-   [ ] T033 [US1] Implement `rag-service/src/retrieval/chapter_retrieval.py` for filtering Qdrant/Postgres by `chapter_id`.
-   [ ] T034 [US1] Implement `rag-service/src/services/summarization_service.py` with map-reduce or hierarchical summarization logic for chapter content.
-   [ ] T035 [P] [US1] Implement logic in `summarization_service.py` to pre-compute and store chapter summaries in Neon Postgres (`chapter_summaries` table).
-   [ ] T036 [US1] Update `POST /chat` endpoint in `rag-service/src/main.py` to handle `query_type: 'chapter_summary'`.
-   [ ] T037 [US1] Implement logic to detect embedded questions in summary requests and, if found, include a prompt for separate questioning in the response.
-   [ ] T038 [P] [US1] Refine `rag-service/src/llm/prompts.py` with prompts for chapter summarization, including adaptive format and question prompting.

### US4: Whole-Book Summary Request [P1]

**Goal**: Provide a high-level overview of the entire textbook.

**Independent Test Criteria**: A request for a whole-book summary returns a comprehensive overview derived from chapter summaries.

-   [ ] T039 [US4] Update `rag-service/src/services/summarization_service.py` to retrieve all pre-computed chapter summaries.
-   [ ] T040 [US4] Implement logic in `summarization_service.py` to generate a whole-book summary from chapter summaries.
-   [ ] T041 [P] [US4] Update `POST /chat` endpoint in `rag-service/src/main.py` to handle `query_type: 'book_summary'`.
-   [ ] T042 [P] [US4] Refine `rag-service/src/llm/prompts.py` with a prompt for whole-book summarization.

---

## Phase 4: Integration & Polish (Cross-Cutting Concerns)

**Goal**: Integrate the RAG service with the existing frontend, ensure robustness, and prepare for deployment.

### US6: Chat Interface Integration [P1]

**Independent Test Criteria**: The chatbot UI is functional within Docusaurus, allowing users to interact with the RAG service and receive responses.

-   [ ] T043 [US6] Implement `backend/src/controllers/rag.controller.ts` for Node.js proxy to FastAPI service (if API key protection or other mediation is needed).
-   [ ] T044 [US6] Implement `my-textbook-site/src/components/RAGChatbot.tsx` for the Docusaurus frontend chatbot UI component.
-   [ ] T045 [US6] Integrate `RAGChatbot.tsx` into a Docusaurus page or layout (e.g., `my-textbook-site/src/pages/chatbot.tsx` or as a persistent widget).
-   [ ] T046 [US6] Implement frontend logic to handle user input, display responses, and manage selected text context for explanation queries.

### General Polish and Testing

-   [ ] T047 Implement comprehensive unit tests for `rag-service/src/config.py`, `rag-service/src/db/`, `rag-service/src/ingestion/`, `rag-service/src/llm/`, `rag-service/src/retrieval/`, `rag-service/src/services/`.
-   [ ] T048 Implement integration tests for `rag-service/src/main.py` (FastAPI endpoints).
-   [ ] T049 Implement end-to-end tests covering ingestion, chat interactions, and response validation.
-   [ ] T050 Review and refine all LLM prompts for clarity, accuracy, and adherence to all constraints.
-   [ ] T051 Dockerize the `rag-service` application.
-   [ ] T052 Develop deployment scripts/configurations for the `rag-service`.
-   [ ] T053 Optimize Qdrant collection parameters and indexing for production performance.
-   [ ] T054 Optimize Neon Postgres schema and queries.
-   [ ] T055 Final review of `quickstart.md` for accuracy and completeness.

