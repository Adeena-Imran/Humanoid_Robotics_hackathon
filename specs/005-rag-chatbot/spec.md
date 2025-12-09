# Feature Specification: RAG Chatbot for Book Content

## 1. Overview

This feature introduces a Retrieval-Augmented Generation (RAG) chatbot embedded within the digital textbook. The chatbot's primary purpose is to assist users in navigating and understanding the book's content by providing summaries and explanations based solely on the material presented in the book.

## 2. User Stories

### User Scenarios

1.  **Chapter Summary Request:** A user wants to quickly grasp the main points of a specific chapter.
    *   **Scenario:** The user types "Summarize Chapter X" (e.g., "Summarize Chapter 3") into the chatbot interface. If an additional question is embedded (e.g., "Summarize Chapter 2, but what is a PID controller?"), the summary will be provided first.
    *   **Expected Outcome:** The chatbot provides a concise summary of the specified chapter. If an embedded question was detected, the chatbot will then prompt the user to ask that question separately.

2.  **Selected Text Explanation:** A user encounters a specific passage or term within the book and requires further clarification based only on that selected text.
    *   **Scenario:** The user highlights a section of text in the book and then asks a question (e.g., "Explain this concept" or "What does 'kinematic chain' mean in this context?").
    *   **Expected Outcome:** The chatbot provides an explanation or answer using *only* the content of the selected text.

3.  **Topic-Based Explanation:** A user needs an explanation of a general topic mentioned in the book.
    *   **Scenario:** The user asks "Explain <topic>" (e.g., "Explain inverse kinematics") into the chatbot interface.
    *   **Expected Outcome:** The chatbot provides an explanation of the topic, drawing information only from the book's content.

4.  **Whole-Book Summary Request:** A user wants a high-level overview of the entire textbook.
    *   **Scenario:** The user types "Summarize the whole book" into the chatbot interface.
    *   **Expected Outcome:** The chatbot provides a high-level summary encompassing the main themes and content across all chapters.

5.  **Query Outside Book Content:** A user asks a question about a topic not covered in the book.
    *   **Scenario:** The user asks "What is quantum computing?" (a topic unrelated to humanoid robotics).
    *   **Expected Outcome:** The chatbot responds with the exact phrase: "This topic is not covered in the book."

## 3. Functional Requirements

*   **FR1: Book Content Ingestion:** The system SHALL be able to ingest and process the digital book's content (Markdown files) to create a searchable knowledge base.
*   **FR2: Chapter Summarization:** The system SHALL be able to generate a summary for any specified chapter within the book. If a user's request for a summary contains an embedded question, the system SHALL first provide the chapter summary and then prompt the user to ask the embedded question separately.
*   **FR3: Selected Text Explanation:** The system SHALL provide explanations or answers to user questions using *only* the content from a user-selected text snippet. The system SHALL strictly adhere to the exact boundaries of the selected text, even if this results in an incomplete answer.
*   **FR4: Topic-Based Explanation:** The system SHALL provide explanations for general topics, retrieving relevant information *only* from the book's content.
*   **FR5: Whole-Book Summarization:** The system SHALL generate a high-level summary of the entire book.
*   **FR6: Contextual Awareness:** The system SHALL ensure that all answers and summaries are derived exclusively from the book's content, without introducing external knowledge.
*   **FR7: Hallucination Prevention:** The system SHALL be designed to minimize or eliminate instances of generating factually incorrect or unsupported information.
*   **FR8: Out-of-Scope Response:** If a user's query cannot be answered from the book's content, the system SHALL respond with the exact phrase: "This topic is not covered in the book."
*   **FR9: Chat Interface Integration:** The chatbot functionality SHALL be integrated into the existing digital textbook site, providing a user-friendly interface for interaction.

## 4. Non-Functional Requirements (NFRs)

*   **NFR1: Accuracy:** Explanations and summaries SHALL be factually consistent with the source book content.
*   **NFR2: Latency:** The chatbot SHALL provide responses to user queries within an acceptable timeframe (e.g., <5 seconds for typical queries).
*   **NFR3: Scalability:** The system SHALL be able to handle an increasing volume of book content and user queries without significant performance degradation.
*   **NFR4: Maintainability:** The RAG system components SHALL be modular and easily maintainable, allowing for updates to content processing, LLM integration, or vector database.
*   **NFR5: Chapter Summary Format:** The format of chapter summaries SHALL be adaptive, with the LLM determining the most appropriate presentation (e.g., bullet points, multiple paragraphs, or a concise single paragraph) based on the content being summarized.

## 5. Success Criteria

*   **SC1: Factual Consistency:** 98% of chatbot responses to within-book questions SHALL be factually consistent with the book's content.
*   **SC2: Out-of-Scope Handling:** For 100% of queries on topics demonstrably outside the book's scope, the chatbot SHALL respond with the exact phrase "This topic is not covered in the book."
*   **SC3: Summarization Quality:** Chapter summaries SHALL accurately capture the main points and key concepts of the respective chapters, as judged by human reviewers. Whole-book summaries SHALL provide a coherent overview of the entire text.
*   **SC4: Response Time:** 90% of user queries (excluding initial content ingestion) SHALL receive a response within 5 seconds.
*   **SC5: Integration:** The chatbot SHALL be seamlessly integrated into the existing user interface, providing an intuitive user experience.

## 6. Assumptions

*   **A1: Book Content Stability:** The primary content of the book (Markdown files) is relatively stable, with updates occurring periodically rather than continuously.
*   **A2: Existing UI:** The existing Docusaurus frontend can be extended to include a chatbot interface (e.g., a chat widget or dedicated page).
*   **A3: Backend APIs:** The existing Node.js backend can be extended to support new API endpoints for chatbot interaction.
*   **A4: Access to LLMs:** Access to suitable Large Language Models (LLMs) (e.g., via OpenAI API or similar) is available.
*   **A5: Vector Database:** A vector database (e.g., Qdrant Cloud Free Tier as suggested) can be integrated with the backend for efficient semantic search.

## 7. Key Entities (Data Model)

*   **Book Content:** The raw text and structure from Markdown/MDX files.
*   **Content Chunks:** Smaller, semantically coherent segments of book content.
    *   Attributes: `text` (string), `embedding` (vector), `metadata` (object: `chapter_title`, `section_title`, `source_file`, `page_number` (if applicable)).
*   **Chapter Summaries:** Pre-computed summaries for each chapter.
    *   Attributes: `chapter_title` (string), `summary_text` (string).
*   **User Query:** The text input from the user.
    *   Attributes: `text` (string), `query_type` (enum: 'explanation', 'chapter_summary', 'book_summary'), `context` (string, for selected text).
*   **Chatbot Response:** The generated answer or summary.
    *   Attributes: `response_text` (string), `sources` (array of objects: `source_file`, `section_title`).

## 8. Open Questions / Needs Clarification

*   **Summary Request with Embedded Question:** If a user includes a specific question within a summary request (e.g., "Summarize chapter 2, but what is a PID controller?"), the system SHALL prioritize providing the summary and then prompt the user to ask the embedded question separately.
