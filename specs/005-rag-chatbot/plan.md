# Implementation Plan: RAG Chatbot for Book Content

**Branch**: `005-rag-chatbot` | **Date**: 2025-12-09 | **Spec**: [specs/005-rag-chatbot/spec.md](specs/005-rag-chatbot/spec.md)
**Input**: Feature specification from `/specs/005-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature introduces a Retrieval-Augmented Generation (RAG) chatbot embedded within the digital textbook. The chatbot's primary purpose is to assist users in navigating and understanding the book's content by providing summaries and explanations based solely on the material presented in the book. The tech stack includes OpenAI Agents / ChatKit SDK, FastAPI backend, Neon Serverless Postgres (metadata, logs), and Qdrant Cloud Free Tier (vector database). The chatbot will strictly adhere to the book content, avoid hallucinations, and respond with "This topic is not covered in the book." for out-of-scope queries. It supports chapter summaries, selected-text explanations, topic-based explanations, and whole-book summaries.

## Technical Context

**Language/Version**: NEEDS CLARIFICATION: Should the RAG backend service be implemented using FastAPI (Python) as specified, separate from the existing Node.js backend, or should the RAG logic be integrated directly into the existing Node.js backend?
**Primary Dependencies**: OpenAI Agents / ChatKit SDK, Qdrant Cloud Free Tier (vector database), LLM client libraries (e.g., OpenAI SDK)
**Storage**: Neon Serverless Postgres (metadata, logs), Qdrant Cloud Free Tier (vector database) for embeddings
**Testing**: Existing backend uses `jest`. NEEDS CLARIFICATION: What testing framework should be used for the new RAG service if it's a separate FastAPI/Python application?
**Target Platform**: Linux server (for FastAPI backend), Web browser (for Docusaurus frontend)
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: NFR2: Latency: The chatbot SHALL provide responses to user queries within an acceptable timeframe (e.g., <5 seconds for typical queries).
**Constraints**: FR6: Contextual Awareness: The system SHALL ensure that all answers and summaries are derived exclusively from the book's content, without introducing external knowledge. FR7: Hallucination Prevention: The system SHALL be designed to minimize or eliminate instances of generating factually incorrect or unsupported information. FR8: Out-of-Scope Response: If a user's query cannot be answered from the book's content, the system SHALL respond with the exact phrase: 'This topic is not covered in the book.'
**Scale/Scope**: Chatbot for book content, Docusaurus frontend.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The RAG Chatbot feature aligns well with the project's constitutional framework:

*   **I. Accurate, Structured, and High-Quality Educational Content:** The chatbot's core function is to provide accurate, context-bound information directly from the book, enhancing the educational content's accessibility and utility.
*   **II. Docusaurus Optimization:** The frontend integration of the chatbot will be optimized for the Docusaurus platform, ensuring a seamless user experience within the existing documentation framework.
*   **III. Modularity, Scalability, and Reusability:** The RAG architecture, particularly if implemented as a separate service, inherently promotes modularity and scalability. The RAG logic and knowledge base can be reused for other content modules.
*   **IV. Clarity, Correctness, and Explainability:** The strict adherence to the book's content, the refusal to introduce external knowledge, and the explicit prevention of hallucinations directly contribute to the clarity, correctness, and explainability of the information provided.
*   **V. Safety:** By restricting the chatbot's knowledge source to the curated book content and preventing external knowledge or hallucinations, the feature inherently contributes to content safety, preventing harmful or unethical outputs.

**Gate Evaluation:** All principles appear to be in alignment, and no immediate violations are identified. The feature passes this initial gate.

## Project Structure

### Documentation (this feature)

```text
specs/005-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

NEEDS CLARIFICATION: If the RAG service is a separate FastAPI application, where should its directory reside in the project structure? (e.g., a new top-level `rag-service/` directory, or within `backend/` as a sub-service?)
```

**Structure Decision**: The project will primarily follow the existing "Web application (frontend + backend)" structure. A decision is pending on the placement of the new RAG service within this structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
