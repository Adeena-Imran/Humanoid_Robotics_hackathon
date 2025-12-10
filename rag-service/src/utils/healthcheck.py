import asyncio
import logging
from ..config.settings import settings
from ..db.neon_client import get_db_connection as check_neon_db_connection
from ..retrieval.semantic_search import QdrantService # For Qdrant connection check
from ..llm.client import LLMClient # Used by QdrantService, ensure it can be initialized
from ..utils.api_errors import InternalServerErrorException

logger = logging.getLogger(__name__)

class HealthCheckService:
    """
    Service responsible for performing startup health checks on external dependencies.
    """

    def __init__(self):
        # Initialize necessary clients for checks
        self.llm_client = LLMClient() # LLMClient depends on API key, will raise ValueError if not set
        self.qdrant_service = QdrantService(self.llm_client)


    async def check_neon_connectivity(self) -> bool:
        """
        Verifies connectivity to the Neon Postgres database.
        """
        logger.info("Performing Neon DB connectivity check...")
        try:
            conn = await check_neon_db_connection()
            # In a real scenario, you might run a simple query like SELECT 1;
            # await execute_query(conn, "SELECT 1;")
            logger.info("Neon DB connectivity check passed.")
            return True
        except InternalServerErrorException as e:
            logger.error(f"Neon DB connectivity check failed: {e.message}")
            return False
        except Exception as e:
            logger.error(f"Neon DB connectivity check failed with unexpected error: {e}")
            return False

    async def check_qdrant_connectivity(self) -> bool:
        """
        Verifies connectivity to the Qdrant vector database.
        """
        logger.info("Performing Qdrant connectivity check...")
        try:
            # Attempt to get collection info, which requires a connection
            await asyncio.wait_for(
                asyncio.to_thread(self.qdrant_service.client.get_collections),
                timeout=settings.QDRANT_SEARCH_TIMEOUT # Use search timeout for connection check
            )
            logger.info("Qdrant connectivity check passed.")
            return True
        except asyncio.TimeoutError:
            logger.error(f"Qdrant connectivity check timed out after {settings.QDRANT_SEARCH_TIMEOUT} seconds.")
            return False
        except Exception as e:
            logger.error(f"Qdrant connectivity check failed with unexpected error: {e}")
            return False

    async def run_startup_checks(self):
        """
        Executes all critical startup health checks. Fails application startup
        if any check is unsuccessful.
        """
        logger.info("Running application startup health checks...")
        
        # Check LLM client initialization (API key presence)
        try:
            # LLMClient is initialized in __init__, if LLM_API_KEY is missing, it would raise ValueError
            _ = self.llm_client 
            logger.info("LLM Client initialized successfully (API key check passed).")
        except ValueError as e:
            logger.critical(f"LLM API Key check failed: {e}. Application cannot start.")
            raise InternalServerErrorException(code="LLM_API_KEY_MISSING", message=str(e), target="LLM_API_KEY")

        neon_ok = await self.check_neon_connectivity()
        qdrant_ok = await self.check_qdrant_connectivity()

        if not (neon_ok and qdrant_ok):
            logger.critical("One or more critical external service checks failed. Application will not start.")
            raise InternalServerErrorException(
                code="EXTERNAL_SERVICE_UNHEALTHY",
                message="Application startup failed due to unhealthy external dependencies (Neon/Qdrant).",
                target="HealthCheck"
            )
        
        logger.info("All startup health checks passed. Application is ready.")

# Example usage (for testing purposes)
async def main():
    logging.basicConfig(level=logging.INFO)
    health_checker = HealthCheckService()
    print("--- Running Startup Checks ---")
    try:
        await health_checker.run_startup_checks()
        print("Application can start.")
    except InternalServerErrorException as e:
        print(f"Application startup aborted: {e.to_api_error().model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Application startup aborted due to unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
