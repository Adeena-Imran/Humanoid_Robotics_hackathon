from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Assuming a structure for retrieved chunks from Qdrant/retrieval system
class RetrievedChunk(BaseModel):
    content: str
    doc_id: str = Field(..., description="Identifier for the source document")
    chunk_id: Optional[str] = Field(None, description="Identifier for the specific chunk within the document")
    score: float = Field(..., description="Relevance score from retrieval")
    chapter_title: Optional[str] = None
    section_title: Optional[str] = None

class GroundedEvidence(BaseModel):
    text: str
    source_id: str # e.g., doc_id or a combination
    chunk_id: Optional[str] = None
    relevance_score: float

class GroundingService:
    """
    Service responsible for processing retrieved chunks and preparing them
    as grounded evidence blocks for answer generation.
    """

    def ground_chunks(self, retrieved_chunks: List[RetrievedChunk]) -> List[GroundedEvidence]:
        """
        Accepts a list of retrieved chunks, attaches source metadata, and prepares
        them as grounded evidence blocks.

        Args:
            retrieved_chunks: A list of RetrievedChunk objects from the retrieval system.

        Returns:
            A list of GroundedEvidence objects, each containing the chunk content
            and its associated source metadata.
        """
        grounded_evidence: List[GroundedEvidence] = []
        for chunk in retrieved_chunks:
            # Combine doc_id and chunk_id (if available) for a unique source_id
            source_id = chunk.doc_id
            if chunk.chunk_id:
                source_id = f"{chunk.doc_id}#{chunk.chunk_id}" # Example: document.md#chunk1

            grounded_evidence.append(
                GroundedEvidence(
                    text=chunk.content,
                    source_id=source_id,
                    chunk_id=chunk.chunk_id,
                    relevance_score=chunk.score
                )
            )
        print(f"Grounded {len(grounded_evidence)} chunks into evidence blocks.")
        return grounded_evidence

    def format_evidence_for_llm(self, grounded_evidence: List[GroundedEvidence]) -> str:
        """
        Formats a list of grounded evidence blocks into a string suitable for LLM consumption.
        Each block is prefixed with a citation marker.

        Args:
            grounded_evidence: A list of GroundedEvidence objects.

        Returns:
            A single string containing all evidence blocks, formatted with citations.
        """
        formatted_blocks = []
        for i, evidence in enumerate(grounded_evidence):
            # Example format: [SOURCE:doc_id#chunk_id] Relevant text from the chunk.
            formatted_blocks.append(f"[SOURCE:{evidence.source_id}] {evidence.text}")
        
        return "\n\n".join(formatted_blocks)


# Example usage
async def main():
    grounding_service = GroundingService()

    # Mock retrieved chunks
    mock_chunks = [
        RetrievedChunk(
            content="Humanoid robots are designed to mimic human form and movement.",
            doc_id="intro_humanoids.md",
            chunk_id="sec1.1",
            score=0.95,
            chapter_title="Introduction",
            section_title="What are Humanoids?"
        ),
        RetrievedChunk(
            content="Kinematics is the study of motion without considering its causes.",
            doc_id="kinematics.md",
            chunk_id="ch2.sec3",
            score=0.88,
            chapter_title="Kinematics",
            section_title="Basic Concepts"
        )
    ]

    print("--- Grounding Chunks ---")
    grounded_evidence = grounding_service.ground_chunks(mock_chunks)
    for evidence in grounded_evidence:
        print(f"Evidence Text: {evidence.text[:50]}...")
        print(f"  Source ID: {evidence.source_id}, Score: {evidence.relevance_score}")

    print("\n--- Formatted Evidence for LLM ---")
    formatted_llm_input = grounding_service.format_evidence_for_llm(grounded_evidence)
    print(formatted_llm_input)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
