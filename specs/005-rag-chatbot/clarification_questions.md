## Question 1: RAG Backend Service Implementation Language and Location

**Context**: The feature description specifies "FastAPI backend" and "OpenAI Agents / ChatKit SDK", which typically implies Python. However, the existing project's `backend/` directory is Node.js/TypeScript. This creates an ambiguity regarding the implementation language and integration approach for the RAG service.

**What we need to know**: Should the RAG backend service be implemented using FastAPI (Python) as specified in the feature description, as a separate application, or should the RAG logic be integrated directly into the existing Node.js backend?

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A      | Implement RAG service as a separate FastAPI (Python) application | Leverages specified tech stack; requires inter-service communication (e.g., HTTP API calls from Node.js to Python); adds operational overhead for a new service. |
| B      | Integrate RAG logic directly into the existing Node.js backend | Simplifies deployment and infrastructure; requires finding/implementing Python-equivalent libraries for specified tech (e.g., OpenAI Agents, Qdrant client, LLM orchestration); may not fully leverage the "FastAPI" mention. |
| C      | Implement RAG logic in Node.js, within the existing backend, but as a distinct module/service layer | Balances integration with modularity; avoids new service deployment; still requires Node.js equivalents for specified tech. |

**Your choice**: _[Wait for user response]_

---

## Question 2: Testing Framework for RAG Service

**Context**: The existing `backend/` uses `jest` for testing. The previous question addresses whether the RAG service will be a separate FastAPI (Python) application or integrated into Node.js. If it's a separate Python application, the testing framework needs to be defined.

**What we need to know**: What testing framework should be used for the new RAG service, assuming it is a separate FastAPI/Python application?

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A      | `pytest` | A widely used and powerful testing framework in the Python ecosystem; good for unit, integration, and functional testing. |
| B      | `unittest` (Python's built-in) | Standard library, no external dependencies; less feature-rich than `pytest` but sufficient for many cases. |
| C      | No separate framework; integrate with existing `jest` (if RAG is Node.js) | Only applicable if the RAG logic is fully integrated into the existing Node.js backend. |

**Your choice**: _[Wait for user response]_

---

## Question 3: Project Structure for Separate RAG Service

**Context**: If the RAG service is decided to be a separate FastAPI (Python) application (Option A in Question 1), its placement within the existing project structure needs to be determined.

**What we need to know**: Where should the directory for a separate FastAPI RAG service reside in the project structure?

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A      | New top-level `rag-service/` directory | Clearly separates the new service; standard practice for polyglot microservice architectures; might require adjustments to build/deployment pipelines. |
| B      | Within `backend/` as a sub-service (e.g., `backend/rag-service/`) | Keeps all backend code under one root; might make `backend/` less cohesive if it mixes Node.js and Python at top-level; deployment could be more complex if `backend/` is treated as a single deployable unit. |

**Your choice**: _[Wait for user response]_

---
I await your choices for these clarification questions. After you provide them, I will update the `plan.md` file and proceed with Phase 0 research.