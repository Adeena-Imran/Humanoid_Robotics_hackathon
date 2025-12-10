from typing import List
from pydantic import BaseModel
from ..llm.client import LLMClient
from .grounding_service import GroundedEvidence # Import GroundedEvidence from grounding_service
import re

class GeneratedAnswer(BaseModel):
    answer: str
    citations: List[str] # List of unique source_ids cited

class AnswerGenerationService:
    """
    Service responsible for generating answers based on grounded evidence,
    including citation markers.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def generate_answer(self, query: str, grounded_evidence: List[GroundedEvidence]) -> GeneratedAnswer:
        """
        Generates an answer based on the provided grounded evidence.
        Requires grounded evidence and attaches citation markers.

        Args:
            query: The original user query.
            grounded_evidence: A list of GroundedEvidence objects.

        Returns:
            A GeneratedAnswer object containing the answer and extracted citations.

        Raises:
            ValueError: If the grounded_evidence list is empty.
        """
        if not grounded_evidence:
            raise ValueError("Cannot generate answer: Grounded evidence is empty.")

        # Prepare context for the LLM
        context_blocks = []
        unique_sources = set()
        for i, evidence in enumerate(grounded_evidence):
            # Format each piece of evidence with a temporary citation for the LLM
            # We will re-parse and format the citations more cleanly after LLM generation
            context_blocks.append(f"[EVIDENCE_BLOCK_{i+1}] {evidence.text}")
            unique_sources.add(evidence.source_id)
        
        formatted_context = "\n\n".join(context_blocks)
        
        # LLM Prompt: Instruct the LLM to use the provided evidence and cite it
        prompt = f"""You are a helpful assistant. Answer the following query based SOLELY on the provided evidence.
If the evidence does not contain the information to answer the query, state that you cannot answer from the given information.
For each statement you make, cite the EVIDENCE_BLOCK it came from using the format [citation:EVIDENCE_BLOCK_X].
Do NOT invent information or make assumptions.

Query: {query}

Evidence:
{formatted_context}

Answer:"""

        llm_raw_response = await self.llm_client.generate_text(prompt, temperature=0.2)

        # Post-process LLM response to attach proper citation markers
        final_answer = self._replace_llm_citations_with_doc_ids(llm_raw_response, grounded_evidence)
        
        # Extract unique citations from the final answer
        extracted_citations = sorted(list(self._extract_citations_from_text(final_answer)))

        return GeneratedAnswer(answer=final_answer, citations=extracted_citations)

    def _replace_llm_citations_with_doc_ids(self, llm_response: str, grounded_evidence: List[GroundedEvidence]) -> str:
        """
        Replaces temporary EVIDENCE_BLOCK_X citations from LLM with actual doc_ids.
        """
        response_with_doc_citations = llm_response
        unique_cited_doc_ids = set()

        for i, evidence in enumerate(grounded_evidence):
            temp_citation_llm = f"[citation:EVIDENCE_BLOCK_{i+1}]"
            # Ensure we replace with the actual source_id, not just doc_id if chunk_id is present
            actual_source_id = evidence.source_id
            new_citation = f"[source:{actual_source_id}]"
            
            response_with_doc_citations = response_with_doc_citations.replace(temp_citation_llm, new_citation)
            if new_citation in response_with_doc_citations:
                unique_cited_doc_ids.add(actual_source_id)

        # Remove any remaining [citation:EVIDENCE_BLOCK_X] that the LLM might have hallucinated or if not replaced
        response_with_doc_citations = re.sub(r"[citation:EVIDENCE_BLOCK_\d+]", "", response_with_doc_citations)
        
        # Ensure citations appear only once at the end of the sentence or block
        # This is a simplification; a more robust solution might handle multiple citations per sentence.
        for doc_id in unique_cited_doc_ids:
            # Avoid adding duplicate citations if LLM already produced it or if it's naturally there
            if f"[source:{doc_id}]" in response_with_doc_citations:
                pass # Already present, nothing to do or handle as a separate pass
            else:
                # This branch means LLM did not generate the citation for this source,
                # which would be a hallucination in the other direction.
                pass # For this task, we focus on what LLM produces.

        return response_with_doc_citations

    def _extract_citations_from_text(self, text: str) -> List[str]:
        """
        Extracts unique citation markers (e.g., [source:doc_id]) from the generated text.
        """
        citations = re.findall(r"[source:([a-zA-Z0-9_#.-]+)]", text)
        return list(set(citations))


# Example usage (for testing purposes)
async def main():
    class MockLLMClient:
        async def generate_text(self, prompt: str, **kwargs) -> str:
            if "empty evidence" in prompt:
                return "I cannot answer based on empty evidence."
            if "humanoid robots" in prompt:
                return "Humanoid robots are machines designed to mimic human appearance and behavior [citation:EVIDENCE_BLOCK_1]. They are used in research and tasks requiring human-like interaction [citation:EVIDENCE_BLOCK_2]."
            return "Generated answer based on the provided query and evidence."

    mock_llm_client = MockLLMClient()
    answer_service = AnswerGenerationService(mock_llm_client)

    # Mock grounded evidence
    mock_evidence_1 = [
        GroundedEvidence(
            text="Humanoid robots are often used in research for bipedal locomotion.",
            source_id="doc_a.md#chunk1",
            relevance_score=0.9
        ),
        GroundedEvidence(
            text="They can also assist in tasks requiring fine motor skills in structured environments.",
            source_id="doc_b.md#chunk2",
            relevance_score=0.8
        )
    ]

    print("--- Generating Answer with Evidence ---")
    try:
        answer_1 = await answer_service.generate_answer("What are humanoid robots used for?", mock_evidence_1)
        print(f"Answer: {answer_1.answer}")
        print(f"Citations: {answer_1.citations}")
    except ValueError as e:
        print(f"Error: {e}")

    print("\n--- Generating Answer with Empty Evidence ---")
    try:
        answer_2 = await answer_service.generate_answer("What is the capital of France?", [])
        print(f"Answer: {answer_2.answer}")
        print(f"Citations: {answer_2.citations}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
