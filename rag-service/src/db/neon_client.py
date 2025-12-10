import asyncio
from typing import Any, Optional
from ..utils.api_errors import InternalServerErrorException
from ..config.settings import settings

async def get_db_connection() -> Any:
    """
    Simulates an asynchronous connection to a Neon database with a timeout.
    In a real scenario, this would use a library like `asyncpg` and `settings.NEON_DATABASE_URL`.
    """
    try:
        # Simulate a database connection process
        await asyncio.wait_for(asyncio.sleep(0.1), timeout=settings.NEON_CONNECTION_TIMEOUT)
        print("Connected to Neon database (mock).")
        # In a real implementation:
        # conn = await asyncpg.connect(settings.NEON_DATABASE_URL)
        return "mock_neon_connection" # Return a mock connection object
    except asyncio.TimeoutError:
        raise InternalServerErrorException(
            code="DB_CONNECTION_TIMEOUT",
            message=f"Neon database connection timed out after {settings.NEON_CONNECTION_TIMEOUT} seconds.",
            target="NeonDB"
        )
    except Exception as e:
        raise InternalServerErrorException(
            code="DB_CONNECTION_FAILED",
            message=f"Failed to connect to Neon database: {e}",
            target="NeonDB"
        )

async def execute_query(conn: Any, query: str, params: Optional[tuple] = None) -> Any:
    """
    Simulates executing a database query with a timeout.
    """
    try:
        await asyncio.wait_for(asyncio.sleep(0.05), timeout=settings.NEON_CONNECTION_TIMEOUT)
        print(f"Executed query: {query} (mock).")
        return "mock_query_result"
    except asyncio.TimeoutError:
        raise InternalServerErrorException(
            code="DB_QUERY_TIMEOUT",
            message=f"Neon database query timed out after {settings.NEON_CONNECTION_TIMEOUT} seconds.",
            target="NeonDB"
        )
    except Exception as e:
        raise InternalServerErrorException(
            code="DB_QUERY_FAILED",
            message=f"Failed to execute Neon database query: {e}",
            target="NeonDB"
        )

# Example usage
async def main():
    print("--- Testing Neon Connection with Timeout ---")
    try:
        conn = await get_db_connection()
        print(f"Successfully got connection: {conn}")
        await execute_query(conn, "SELECT 1")
    except InternalServerErrorException as e:
        print(f"Error: {e.to_api_error().model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n--- Testing Neon Connection Timeout (simulated) ---")
    original_timeout = settings.NEON_CONNECTION_TIMEOUT
    # Temporarily override setting for testing purposes
    settings.NEON_CONNECTION_TIMEOUT = 0.01 
    try:
        await get_db_connection()
    except InternalServerErrorException as e:
        print(f"Error: {e.to_api_error().model_dump_json(indent=2)}")
    finally:
        settings.NEON_CONNECTION_TIMEOUT = original_timeout # Reset setting

if __name__ == "__main__":
    asyncio.run(main())