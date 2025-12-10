import pytest
import asyncio
from unittest.mock import AsyncMock, patch

# Import the services and models to be tested
from rag-service.src.services.grounding_service import GroundingService, RetrievedChunk, GroundedEvidence
from rag-service.src.services.answer_generation_service import AnswerGenerationService, GeneratedAnswer
from rag-service.src.services.hallucination_guard import HallucinationGuardService
from rag-service.src.llm.client import LLMClient
from rag-service.src.main import REFUSAL_RESPONSE, CONFIDENCE_THRESHOLD # Import for main app logic test

# Mock for semantic_search which typically returns ContentChunk
class MockContentChunk:
    def __init__(self, content, source_file, chapter_title, section_title):
        self.content = content
        self.source_file = source_file
        self.chapter_title = chapter_title
        self.section_title = section_title

@pytest.fixture
def mock_llm_client():
    """Fixture for mocking the LLMClient."""
    return AsyncMock(spec=LLMClient)

@pytest.fixture
def grounding_service():
    return GroundingService()

@pytest.fixture
def answer_generation_service(mock_llm_client):
    return AnswerGenerationService(mock_llm_client)

@pytest.fixture
def hallucination_guard_service(mock_llm_client):
    return HallucinationGuardService(mock_llm_client)

@pytest.mark.asyncio
async def test_answer_includes_citations(
    mock_llm_client, grounding_service, answer_generation_service
):
    """
    Validate that generated answers include citations.
    """
    query = "What is bipedal locomotion?"
    mock_retrieved_chunks = [
        RetrievedChunk(
            content="Bipedal locomotion refers to movement using two legs.",
            doc_id="locomotion.md",
            chunk_id="sec1",
            score=0.9,
        ),
        RetrievedChunk(
            content="Humanoid robots often employ bipedal locomotion for stability.",
            doc_id="robots.md",
            chunk_id="sec2",
            score=0.8,
        ),
    ]

    mock_llm_client.generate_text.return_value = (
        "Bipedal locomotion is movement on two legs [citation:EVIDENCE_BLOCK_1]. "
        "Humanoid robots use this for stability [citation:EVIDENCE_BLOCK_2]."
    )

    grounded_evidence = grounding_service.ground_chunks(mock_retrieved_chunks)
    generated_answer = await answer_generation_service.generate_answer(
        query, grounded_evidence
    )

    assert "Bipedal locomotion is movement on two legs [source:locomotion.md#sec1]. " in generated_answer.answer
    assert "Humanoid robots use this for stability [source:robots.md#sec2]." in generated_answer.answer
    assert "locomotion.md#sec1" in generated_answer.citations
    assert "robots.md#sec2" in generated_answer.citations


@pytest.mark.asyncio
async def test_refusal_when_evidence_missing(answer_generation_service):
    """
    Validate refusal to generate an answer when grounded evidence is empty.
    """
    query = "Why is the sky blue?"
    with pytest.raises(ValueError, match="Grounded evidence is empty."):
        await answer_generation_service.generate_answer(query, [])


@pytest.mark.asyncio
async def test_hallucination_score_behavior(
    mock_llm_client, grounding_service, hallucination_guard_service
):
    """
    Validate the behavior of the hallucination guard's confidence score.
    """
    # Mock data
    grounded_evidence = [
        GroundedEvidence(text="Fact A is true.", source_id="doc_a", relevance_score=0.9),
        GroundedEvidence(text="Fact B is true.", source_id="doc_b", relevance_score=0.8),
    ]

    # Test 1: Fully grounded answer
    generated_fully_grounded = GeneratedAnswer(
        answer="Fact A is true [source:doc_a]. Fact B is also true [source:doc_b].",
        citations=["doc_a", "doc_b"],
    )
    confidence = await hallucination_guard_service.check_answer_grounding(
        generated_fully_grounded, grounded_evidence
    )
    assert confidence == 1.0

    # Test 2: Partially grounded (one valid, one invalid citation)
    generated_partially_grounded = GeneratedAnswer(
        answer="Fact A is true [source:doc_a]. Fact C is true [source:doc_c].",
        citations=["doc_a", "doc_c"],
    )
    confidence = await hallucination_guard_service.check_answer_grounding(
        generated_partially_grounded, grounded_evidence
    )
    assert confidence == 0.5  # 1 valid citation out of 2 total cited

    # Test 3: Ungrounded (all invalid citations)
    generated_ungrounded = GeneratedAnswer(
        answer="Fact X is true [source:doc_x].", citations=["doc_x"]
    )
    confidence = await hallucination_guard_service.check_answer_grounding(
        generated_ungrounded, grounded_evidence
    )
    assert confidence == 0.0

    # Test 4: No citations, but evidence exists
    generated_no_citations = GeneratedAnswer(answer="Some answer here.", citations=[])
    confidence = await hallucination_guard_service.check_answer_grounding(
        generated_no_citations, grounded_evidence
    )
    assert confidence == 0.5 # Default for no citations but evidence exists

    # Test 5: Empty answer, evidence exists
    generated_empty_answer = GeneratedAnswer(answer="", citations=[])
    confidence = await hallucination_guard_service.check_answer_grounding(
        generated_empty_answer, grounded_evidence
    )
    assert confidence == 0.1

    # Test 6: No evidence provided to the guard
    generated_any_answer = GeneratedAnswer(answer="Answer.", citations=["doc_a"])
    confidence = await hallucination_guard_service.check_answer_grounding(
        generated_any_answer, []
    )
    assert confidence == 0.0

@pytest.mark.asyncio
@patch("rag-service.src.retrieval.semantic_search")
async def test_chat_endpoint_refusal_low_confidence(
    mock_semantic_search,
    mock_llm_client,
    grounding_service,
    answer_generation_service,
    hallucination_guard_service,
):
    """
    Validate that the /chat endpoint returns a refusal message when hallucination confidence is low.
    """
    from rag_service.src.main import (
        app,
        grounding_service_instance,
        answer_generation_service_instance,
        hallucination_guard_service_instance,
        llm_client_instance # We need to ensure the real instances are used here or mocked appropriately
    )
    from fastapi.testclient import TestClient

    # Patch the instances used in main.py
    with patch("rag_service.src.main.grounding_service_instance", grounding_service), \
         patch("rag_service.src.main.answer_generation_service_instance", answer_generation_service), \
         patch("rag_service.src.main.hallucination_guard_service_instance", hallucination_guard_service), \
         patch("rag_service.src.main.llm_client_instance", mock_llm_client): # Ensure LLMClient is also patched in main

        client = TestClient(app)

        # Mock semantic_search to return chunks
        mock_semantic_search.return_value = [
            MockContentChunk(
                content="This is some relevant content for grounding.",
                source_file="grounding_doc.md",
                chapter_title="Grounding",
                section_title="Introduction",
            )
        ]

        # Mock LLM to generate an answer with invalid citations (leading to low confidence)
        mock_llm_client.generate_text.return_value = (
            "This answer is completely made up [citation:EVIDENCE_BLOCK_1] and not in the evidence [citation:EVIDENCE_BLOCK_2]."
        )
        
        # We need to manually construct the GeneratedAnswer that answer_generation_service_instance
        # would return if it were called with the mocked LLM response.
        # This is a bit tricky since answer_generation_service_instance also uses the LLM client.
        # A simpler approach for this specific test would be to mock hallucination_guard_service.check_answer_grounding
        # directly to return a low confidence.

        # Let's mock hallucination_guard_service.check_answer_grounding directly to control confidence
        hallucination_guard_service.check_answer_grounding.return_value = 0.2 # Below CONFIDENCE_THRESHOLD

        response = client.post(
            "/chat", json={"query_type": "explanation", "text": "Some query"}
        )

        assert response.status_code == 200
        assert response.json()["response"] == "I cannot confidently answer your question based on the available information. Please try rephrasing or asking a different question."
        assert response.json()["citations"] == []

@pytest.mark.asyncio
@patch("rag-service.src.retrieval.semantic_search")
async def test_chat_endpoint_valid_answer_with_citations(
    mock_semantic_search,
    mock_llm_client,
    grounding_service,
    answer_generation_service,
    hallucination_guard_service,
):
    """
    Validate that the /chat endpoint returns a valid answer with citations when confidence is high.
    """
    from rag_service.src.main import (
        app,
        grounding_service_instance,
        answer_generation_service_instance,
        hallucination_guard_service_instance,
        llm_client_instance
    )
    from fastapi.testclient import TestClient

    with patch("rag_service.src.main.grounding_service_instance", grounding_service), \
         patch("rag_service.src.main.answer_generation_service_instance", answer_generation_service), \
         patch("rag_service.src.main.hallucination_guard_service_instance", hallucination_guard_service), \
         patch("rag_service.src.main.llm_client_instance", mock_llm_client):

        client = TestClient(app)

        # Mock semantic_search to return chunks
        mock_semantic_search.return_value = [
            MockContentChunk(
                content="Relevant info A. [source:doc_a]",
                source_file="doc_a",
                chapter_title="Chapter 1",
                section_title="Sec A",
            ),
            MockContentChunk(
                content="Relevant info B. [source:doc_b]",
                source_file="doc_b",
                chapter_title="Chapter 1",
                section_title="Sec B",
            ),
        ]

        # Mock LLM to generate an answer that uses the provided evidence and cites correctly
        mock_llm_client.generate_text.return_value = (
            "The answer is info A [citation:EVIDENCE_BLOCK_1] and info B [citation:EVIDENCE_BLOCK_2]."
        )
        
        # Mock hallucination guard to return high confidence
        hallucination_guard_service.check_answer_grounding.return_value = 0.9 # Above CONFIDENCE_THRESHOLD

        response = client.post(
            "/chat", json={"query_type": "explanation", "text": "What is A and B?"}
        )

        assert response.status_code == 200
        assert "The answer is info A [source:doc_a] and info B [source:doc_b]." in response.json()["response"]
        assert "doc_a" in response.json()["citations"]
        assert "doc_b" in response.json()["citations"]
        assert len(response.json()["sources"]) == 2 # Check if original sources are also returned
