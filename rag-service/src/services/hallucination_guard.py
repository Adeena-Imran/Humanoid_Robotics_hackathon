from typing import List
from ..llm.client import LLMClient
from .grounding_service import GroundedEvidence
from .answer_generation_service import GeneratedAnswer
import re

class HallucinationGuardService:
    """
    Service responsible for detecting unsupported claims (hallucinations) in a generated answer
    by comparing it against the provided grounded evidence.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def check_answer_grounding(
        self,
        generated_answer: GeneratedAnswer,
        grounded_evidence: List[GroundedEvidence]
    ) -> float:
        """
        Compares the generated answer with the grounded evidence to detect unsupported claims
        and returns a confidence score (0-1).

        Args:
            generated_answer: The GeneratedAnswer object containing the answer and its citations.
            grounded_evidence: The list of GroundedEvidence objects used for generation.

        Returns:
            A float representing the confidence score (0-1). 1 means fully grounded,
            0 means entirely ungrounded or contradictory.
        """
        if not grounded_evidence:
            # If there was no evidence, the answer cannot be grounded.
            # However, `answer_generation_service` should prevent generation in this case.
            # If an answer still slipped through without evidence, it's 0 confidence.
            return 0.0

        # Extract all available source_ids from the grounded evidence
        available_source_ids = {evidence.source_id for evidence in grounded_evidence}

        # Check citations in the generated answer
        all_cited_sources_in_answer = set(generated_answer.citations)

        # Count how many cited sources are actually present in the provided evidence
        grounded_citations_count = len(available_source_ids.intersection(all_cited_sources_in_answer))
        
        # Calculate a simple confidence based on citations
        # If there are citations, how many are valid?
        # If no citations, but there was evidence, this simple metric won't catch LLM not citing.
        confidence_from_citations = 0.0
        if len(all_cited_sources_in_answer) > 0:
            confidence_from_citations = grounded_citations_count / len(all_cited_sources_in_answer)
        elif len(grounded_evidence) > 0 and len(all_cited_sources_in_answer) == 0:
            # If evidence was provided but LLM didn't cite anything, it's a weak signal.
            # Could be a sign of hallucination or simply poor citation generation.
            # For this simple model, let's give a small penalty.
            confidence_from_citations = 0.5 if len(available_source_ids) > 0 else 0.0

        # More advanced check: Use LLM to verify each statement against evidence
        # This is a placeholder for a more sophisticated check.
        # For a full implementation, you might pass the answer and evidence back to an LLM
        # to explicitly rate its grounding or rephrase it only using evidence.
        # prompt = f"""Given the evidence: {grounded_text} and the answer: {generated_answer.answer}.
        # Is every statement in the answer directly supported by the evidence? Rate confidence (0-1)."""
        # llm_confidence_response = await self.llm_client.generate_text(prompt)
        # llm_confidence = float(llm_confidence_response) # Parse score

        # For this task, we will simplify: if all cited sources are valid, confidence is high.
        # We can further penalize if the answer is completely devoid of content despite evidence.
        if generated_answer.answer.strip() == "" and len(grounded_evidence) > 0:
            return 0.1 # Very low confidence if answer is empty but evidence existed

        return confidence_from_citations # This is our primary score for now

# Example usage (for testing purposes)
async def main():
    class MockLLMClient:
        async def generate_text(self, prompt: str, **kwargs) -> str:
            return "Mock LLM response for grounding check." # Not used in current simple impl

    mock_llm_client = MockLLMClient()
    hallucination_guard = HallucinationGuardService(mock_llm_client)

    # Mock Grounded Evidence
    evidence_1 = GroundedEvidence(text="Robots use sensors.", source_id="doc_sensor.md", relevance_score=0.9)
    evidence_2 = GroundedEvidence(text="Motors drive robot movement.", source_id="doc_motor.md", relevance_score=0.8)
    all_grounded_evidence = [evidence_1, evidence_2]

    print("---\n--- Test Case 1: Fully Grounded Answer ---")
    generated_answer_good = GeneratedAnswer(
        answer="Robots utilize sensors for perception [source:doc_sensor.md] and motors for motion [source:doc_motor.md].",
        citations=["doc_sensor.md", "doc_motor.md"]
    )
    confidence = await hallucination_guard.check_answer_grounding(generated_answer_good, all_grounded_evidence)
    print(f"Confidence (Good Answer): {confidence}")
    assert confidence == 1.0

    print("\n--- Test Case 2: Partially Grounded Answer (one invalid citation) ---")
    generated_answer_partial = GeneratedAnswer(
        answer="Robots use sensors [source:doc_sensor.md] and also have AI [source:doc_ai.md].",
        citations=["doc_sensor.md", "doc_ai.md"]
    )
    confidence_partial = await hallucination_guard.check_answer_grounding(generated_answer_partial, all_grounded_evidence)
    print(f"Confidence (Partial Answer): {confidence_partial}")
    # Expected: 1 valid / 2 total citations = 0.5
    assert confidence_partial == 0.5

    print("\n--- Test Case 3: Ungrounded Answer (no valid citations) ---")
    generated_answer_bad = GeneratedAnswer(
        answer="Robots are living beings [source:doc_biology.md].",
        citations=["doc_biology.md"]
    )
    confidence_bad = await hallucination_guard.check_answer_grounding(generated_answer_bad, all_grounded_evidence)
    print(f"Confidence (Bad Answer): {confidence_bad}")
    assert confidence_bad == 0.0

    print("\n--- Test Case 4: Answer with no citations but evidence exists (should get a penalty) ---")
    generated_answer_no_citations = GeneratedAnswer(
        answer="Robots can move.",
        citations=[]
    )
    confidence_no_citations = await hallucination_guard.check_answer_grounding(generated_answer_no_citations, all_grounded_evidence)
    print(f"Confidence (No Citations): {confidence_no_citations}")
    assert confidence_no_citations == 0.5

    print("\n--- Test Case 5: Empty Answer with evidence ---")
    generated_answer_empty = GeneratedAnswer(
        answer="",
        citations=[]
    )
    confidence_empty = await hallucination_guard.check_answer_grounding(generated_answer_empty, all_grounded_evidence)
    print(f"Confidence (Empty Answer): {confidence_empty}")
    assert confidence_empty == 0.1

    print("\n--- Test Case 6: No Evidence Provided ---")
    generated_answer_no_evidence = GeneratedAnswer(
        answer="Any answer here is ungrounded.",
        citations=["doc_random.md"]
    )
    confidence_no_evidence = await hallucination_guard.check_answer_grounding(generated_answer_no_evidence, [])
    print(f"Confidence (No Evidence): {confidence_no_evidence}")
    assert confidence_no_evidence == 0.0


if __name__ == "__main__":
    asyncio.run(main())
