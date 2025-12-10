import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

# Import components from the main application
from rag-service.src.main import app, REFUSAL_RESPONSE
from rag-service.src.utils.api_errors import (
    BadRequestException,
    TooManyRequestsException,
    APIError,
    ErrorDetail,
    InternalServerErrorException,
    NotFoundException
)
from rag-service.src.utils.request_validator import ALLOWED_QUERY_TYPES
from rag-service.src.middleware.rate_limiter import (
    _rate_limit_store, # Import the in-memory store for resetting
)
from rag-service.src.config.settings import settings # Import settings

# Mock semantic_search for tests
class MockContentChunk:
    def __init__(self, content, source_file, chapter_title, section_title):
        self.content = content
        self.source_file = source_file
        self.chapter_title = chapter_title
        self.section_title = section_title

@pytest.fixture(autouse=True)
def reset_rate_limit_store():
    """Resets the in-memory rate limit store before each test."""
    _rate_limit_store.clear()
    yield

@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)

@pytest.fixture
def mock_llm_client():
    """Fixture for mocking the LLMClient."""
    return AsyncMock(spec_set=["generate_text", "get_embedding"])

@pytest.fixture(autouse=True)
def mock_services_for_main_app(mock_llm_client):
    """
    Patch necessary services in main.py for isolation during API hardening tests.
    """
    with patch(
        "rag-service.src.main.llm_client_instance", mock_llm_client
    ), patch(
        "rag-service.src.main.subagent_service_instance", AsyncMock()
    ), patch(
        "rag-service.src.main.skill_service_instance", AsyncMock()
    ), patch(
        "rag-service.src.main.context_service_instance", AsyncMock()
    ), patch(
        "rag-service.src.main.grounding_service_instance", AsyncMock()
    ), patch(
        "rag-service.src.main.answer_generation_service_instance", AsyncMock()
    ), patch(
        "rag-service.src.main.hallucination_guard_service_instance", AsyncMock()
    ), patch(
        "rag-service.src.retrieval.semantic_search", AsyncMock()
    ) as mock_semantic_search:
        # Configure mocks if needed for specific test cases
        yield mock_semantic_search


@pytest.mark.asyncio
async def test_invalid_payload_rejected(client):
    """
    Validate that an invalid payload is rejected with a standardized error.
    """
    # Missing session_id
    response = client.post(
        "/chat", json={"query_type": "explanation", "text": "test query"}
    )
    assert response.status_code == 400
    error = APIError(**response.json())
    assert error.error.code == "VALIDATION_ERROR"
    assert "session_id is required" in error.error.message
    assert error.error.target == "session_id"

    # Invalid query_type
    response = client.post(
        "/chat",
        json={
            "session_id": "test_session",
            "query_type": "invalid_type",
            "text": "test query",
        },
    )
    assert response.status_code == 400
    error = APIError(**response.json())
    assert error.error.code == "VALIDATION_ERROR"
    assert "Invalid query_type" in error.error.message
    assert error.error.target == "query_type"

    # Missing text for explanation
    response = client.post(
        "/chat", json={"session_id": "test_session", "query_type": "explanation"}
    )
    assert response.status_code == 400
    error = APIError(**response.json())
    assert error.error.code == "VALIDATION_ERROR"
    assert "text (query) is required" in error.error.message
    assert error.error.target == "text"

    # Invalid subagent format
    response = client.post(
        "/chat",
        json={
            "session_id": "test_session",
            "query_type": "subagent",
            "text": "just_subagent_name",
        },
    )
    assert response.status_code == 400
    error = APIError(**response.json())
    assert error.error.code == "VALIDATION_ERROR"
    assert "For 'subagent' query_type, 'text' must be in 'subagent_name: skill_name' format." in error.error.message
    assert error.error.target == "text"


@pytest.mark.asyncio
async def test_rate_limiting_enforced(client):
    """
    Validate that rate limiting is enforced and returns a standardized error.
    """
    session_id = "rate_limit_session"
    payload = {"session_id": session_id, "query_type": "explanation", "text": "hello"}

    # Send settings.RATE_LIMIT_MAX_REQUESTS number of requests - these should succeed
    for _ in range(settings.RATE_LIMIT_MAX_REQUESTS):
        response = client.post("/chat", json=payload)
        assert response.status_code != 429 # Should not be rate-limited yet

    # The (MAX_REQUESTS + 1)th request should be rate-limited
    response = client.post("/chat", json=payload)
    assert response.status_code == 429
    error = APIError(**response.json())
    assert error.error.code == "TOO_MANY_REQUESTS"
    assert f"Rate limit exceeded. Max {settings.RATE_LIMIT_MAX_REQUESTS} requests per {settings.RATE_LIMIT_TIME_WINDOW_SECONDS} seconds." in error.error.message
    assert error.error.target == "session_id"


@pytest.mark.asyncio
async def test_errors_returned_in_standardized_format(client, mock_semantic_search):
    """
    Validate that various internal errors are caught and returned in the standardized format.
    """
    session_id = "error_test_session"
    payload = {"session_id": session_id, "query_type": "explanation", "text": "trigger error"}

    # Simulate an internal server error (e.g., from semantic_search)
    mock_semantic_search.side_effect = InternalServerErrorException(
        code="DB_ISSUE", message="Database connection lost"
    )
    response = client.post("/chat", json=payload)

    assert response.status_code == 500
    error = APIError(**response.json())
    assert error.error.code == "DB_ISSUE"
    assert "Database connection lost" in error.error.message
    assert error.error.target is None

    # Simulate a NotFoundException (e.g., if a subagent is not found)
    # We need to explicitly trigger this, as subagent lookup is mocked.
    with patch(
        "rag-service.src.main.subagent_service_instance.get_subagent"
    ) as mock_get_subagent:
        mock_get_subagent.return_value = None # Subagent not found
        subagent_payload = {
            "session_id": session_id,
            "query_type": "subagent",
            "text": "non_existent_agent:some_skill",
        }
        response = client.post("/chat", json=subagent_payload)
        assert response.status_code == 404
        error = APIError(**response.json())
        assert error.error.code == "NOT_FOUND"
        assert "Subagent 'non_existent_agent' not found." in error.error.message
        assert error.error.target is None