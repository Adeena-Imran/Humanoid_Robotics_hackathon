import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import os

# Import necessary components for testing
from rag_service.src.main import app
from rag_service.src.config.settings import Settings, settings as app_settings # Renamed settings to app_settings to avoid conflict
from rag_service.src.utils.healthcheck import HealthCheckService
from rag_service.src.utils.api_errors import InternalServerErrorException
from rag_service.src.db.neon_client import get_db_connection as neon_get_db_connection
from rag_service.src.retrieval.semantic_search import QdrantService
from rag_service.src.llm.client import LLMClient

# Fixture to reset environment variables after each test
@pytest.fixture(autouse=True)
def clean_env_vars():
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def health_check_service():
    """Fixture to provide a HealthCheckService instance."""
    # Ensure LLMClient initialization within HealthCheckService doesn't fail prematurely
    with patch('rag_service.src.llm.client.LLMClient.__init__', return_value=None), \
         patch('rag_service.src.llm.client.LLMClient.generate_text', new_callable=AsyncMock), \
         patch('rag_service.src.llm.client.LLMClient.get_embedding', new_callable=AsyncMock):
        
        # Mock QdrantService client attribute, as it's accessed by check_qdrant_connectivity
        with patch('rag_service.src.retrieval.semantic_search.QdrantClient') as MockQdrantClient:
            mock_qdrant_client_instance = MockQdrantClient.return_value
            mock_qdrant_client_instance.get_collections = AsyncMock(return_value=None)
            
            hc = HealthCheckService()
            hc.llm_client.api_key = "mock_key" # Ensure it thinks API key is set for internal init check
            hc.qdrant_service = QdrantService(hc.llm_client) # Re-initialize QdrantService with mocked LLM
            yield hc


@pytest.mark.asyncio
async def test_app_fails_on_missing_llm_api_key():
    """
    Validate that the application fails startup if LLM_API_KEY is missing.
    """
    # Clear LLM_API_KEY to simulate missing dependency
    del os.environ["LLM_API_KEY"] # Ensure it's not set
    
    with pytest.raises(InternalServerErrorException, match="LLM API Key check failed"):
        # We need to re-instantiate Settings to reflect the changed environment
        # and then HealthCheckService relies on it
        test_settings = Settings()
        test_llm_client = LLMClient() # This will raise ValueError
        test_health_checker = HealthCheckService()
        await test_health_checker.run_startup_checks()

@pytest.mark.asyncio
async def test_health_check_fails_on_neon_unreachable(health_check_service):
    """Validate that health check fails if Neon is unreachable."""
    with patch("rag_service.src.db.neon_client.get_db_connection", AsyncMock(side_effect=Exception("Neon connection error"))):
        with pytest.raises(InternalServerErrorException, match="Application startup failed due to unhealthy external dependencies"):
            await health_check_service.run_startup_checks()

@pytest.mark.asyncio
async def test_health_check_fails_on_qdrant_unreachable(health_check_service):
    """Validate that health check fails if Qdrant is unreachable."""
    with patch("rag_service.src.retrieval.semantic_search.QdrantClient") as MockQdrantClient:
        mock_qdrant_client_instance = MockQdrantClient.return_value
        mock_qdrant_client_instance.get_collections.side_effect = Exception("Qdrant connection error")
        
        # Re-initialize QdrantService within health_check_service to pick up the mock
        health_check_service.qdrant_service = QdrantService(health_check_service.llm_client)

        with pytest.raises(InternalServerErrorException, match="Application startup failed due to unhealthy external dependencies"):
            await health_check_service.run_startup_checks()

@pytest.mark.asyncio
async def test_health_check_succeeds_when_all_healthy(health_check_service):
    """Validate that health check passes when all external services are reachable."""
    with patch("rag_service.src.db.neon_client.get_db_connection", AsyncMock(return_value="mock_conn")), \
         patch("rag_service.src.retrieval.semantic_search.QdrantClient") as MockQdrantClient:
        
        mock_qdrant_client_instance = MockQdrantClient.return_value
        mock_qdrant_client_instance.get_collections.return_value = [] # Simulate successful Qdrant response

        # Ensure LLM_API_KEY is set for this successful path
        os.environ["LLM_API_KEY"] = "test_key"
        
        # Re-instantiate settings and HealthCheckService to reflect new env var
        app_settings.__init__()
        health_check_service = HealthCheckService()

        # Should not raise any exception
        await health_check_service.run_startup_checks()


@pytest.mark.asyncio
async def test_config_loading_per_environment():
    """Validate that configuration settings are loaded correctly from environment variables."""
    # Test defaults
    # Need to clear environment variables for clean default testing
    original_env_llm_key = os.environ.get("LLM_API_KEY")
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]
    
    class TestSettings(Settings):
        model_config = SettingsConfigDict(env_file='.env', extra='ignore') # .env file support, ignore extra fields

    default_settings = TestSettings()
    assert default_settings.LLM_API_KEY == "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    assert default_settings.QDRANT_HOST == "localhost"
    assert default_settings.RATE_LIMIT_MAX_REQUESTS == 5

    # Test overrides from environment variables
    os.environ["LLM_API_KEY"] = "my_llm_key_from_env"
    os.environ["QDRANT_HOST"] = "qdrant.cloud.com"
    os.environ["RATE_LIMIT_MAX_REQUESTS"] = "100"

    env_settings = TestSettings()
    assert env_settings.LLM_API_KEY == "my_llm_key_from_env"
    assert env_settings.QDRANT_HOST == "qdrant.cloud.com"
    assert env_settings.RATE_LIMIT_MAX_REQUESTS == 100 # Pydantic converts to int

    # Restore original LLM_API_KEY if it existed
    if original_env_llm_key is not None:
        os.environ["LLM_API_KEY"] = original_env_llm_key
