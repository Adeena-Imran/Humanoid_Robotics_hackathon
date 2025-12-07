# claude-code/agents/rag_content_agent.py

"""
## RAGContentAgent
**Description:** Prepares textbook content for Retrieval Augmented Generation (RAG) by cleaning text, generating relevant metadata, and formatting it for chunking and storage in a vector database.
**Inputs:**
- Raw textbook content (e.g., Docusaurus Markdown from BookWriterAgent)
**Outputs:**
- JSON objects containing cleaned text chunks, associated metadata (e.g., chapter, section, topic), and chunk identifiers.
**Functions / Capabilities:**
- Text cleaning (removing formatting, extraneous characters)
- Content chunking based on semantic boundaries
- Metadata extraction and generation
- JSON formatting
**Rules:**
- Ensure text chunks are self-contained and semantically coherent for effective retrieval.
- Metadata must be consistent and rich enough to support targeted retrieval.
- Output must be valid JSON.
"""

class RAGContentAgent:
    def __init__(self):
        self.description = "Prepares textbook content for Retrieval Augmented Generation (RAG) by cleaning text, generating relevant metadata, and formatting it for chunking and storage in a vector database."
        self.inputs = [
            "Raw textbook content (e.g., Docusaurus Markdown from BookWriterAgent)"
        ]
        self.outputs = [
            "JSON objects containing cleaned text chunks, associated metadata (e.g., chapter, section, topic), and chunk identifiers."
        ]
        self.functions_capabilities = [
            "Text cleaning (removing formatting, extraneous characters)",
            "Content chunking based on semantic boundaries",
            "Metadata extraction and generation",
            "JSON formatting"
        ]
        self.rules = [
            "Ensure text chunks are self-contained and semantically coherent for effective retrieval.",
            "Metadata must be consistent and rich enough to support targeted retrieval.",
            "Output must be valid JSON."
        ]

    def prepare_for_rag(self, content):
        # Placeholder for actual RAG content preparation logic
        pass
