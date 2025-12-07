# claude-code/skills/prepare_chunks_for_rag_skill.py

"""
## PrepareChunksForRAGSkill
**Description:** Processes a full Docusaurus Markdown chapter to prepare it for Retrieval Augmented Generation (RAG) by cleaning the text, chunking it into embedding-sized pieces, generating relevant metadata (chapter title, tags), and returning the output as JSON suitable for insertion into a Qdrant vector database.
**Inputs:**
- `chapter_markdown`: The complete chapter content in Docusaurus Markdown format.
**Outputs:**
- A JSON string containing an array of objects, where each object represents an embedding-ready chunk with its corresponding text, chapter title, and relevant tags.
**Logic Steps:**
1. Pass the `chapter_markdown` to the `RAGContentAgent` for text cleaning.
2. The `RAGContentAgent` will then chunk the cleaned text into appropriate sizes for embeddings.
3. The `RAGContentAgent` will generate metadata for each chunk, including the chapter title and relevant tags extracted from the content.
4. The `RAGContentAgent` will format the chunks and their metadata into a JSON structure suitable for a vector database like Qdrant.
**Rules:**
- The cleaning process should remove all Docusaurus Markdown specific syntax while preserving the semantic content.
- Chunks should be of a size optimized for embedding models, ensuring semantic coherence within each chunk.
- Metadata (chapter title, tags) must accurately reflect the content of each chunk.
- The final output must be a well-formed JSON string, ready for direct ingestion into a vector database.
"""

import json
from claude_code.agents.rag_content_agent import RAGContentAgent

class PrepareChunksForRAGSkill:
    def __init__(self):
        self.description = "Processes a full Docusaurus Markdown chapter to prepare it for Retrieval Augmented Generation (RAG) by cleaning the text, chunking it into embedding-sized pieces, generating relevant metadata (chapter title, tags), and returning the output as JSON suitable for insertion into a Qdrant vector database."
        self.inputs = ["chapter_markdown"]
        self.outputs = ["A JSON string containing an array of objects, where each object represents an embedding-ready chunk with its corresponding text, chapter title, and relevant tags."]
        self.logic_steps = [
            "Pass the `chapter_markdown` to the `RAGContentAgent` for text cleaning.",
            "The `RAGContentAgent` will then chunk the cleaned text into appropriate sizes for embeddings.",
            "The `RAGContentAgent` will generate metadata for each chunk, including the chapter title and relevant tags extracted from the content.",
            "The `RAGContentAgent` will format the chunks and their metadata into a JSON structure suitable for a vector database like Qdrant."
        ]
        self.rules = [
            "The cleaning process should remove all Docusaurus Markdown specific syntax while preserving the semantic content.",
            "Chunks should be of a size optimized for embedding models, ensuring semantic coherence within each chunk.",
            "Metadata (chapter title, tags) must accurately reflect the content of each chunk.",
            "The final output must be a well-formed JSON string, ready for direct ingestion into a vector database."
        ]
        self.rag_content_agent = RAGContentAgent()

    def execute(self, chapter_markdown):
        # Placeholder for actual skill execution logic
        # This would call methods on self.rag_content_agent
        cleaned_chunks_with_metadata = self.rag_content_agent.prepare_for_rag(chapter_markdown)
        return json.dumps(cleaned_chunks_with_metadata)
