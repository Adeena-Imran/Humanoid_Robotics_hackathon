# rag-service/src/utils/error_handling.py

import logging
import functools
from datetime import datetime

# Configure logging
# In a real app, this might be configured in a central place
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='error.log' # Example of logging to a file
)
logger = logging.getLogger(__name__)

# --- Custom Exception Classes ---

class RagServiceError(Exception):
    """Base exception class for the RAG service."""
    def __init__(self, message="An unexpected error occurred in the RAG service."):
        self.message = message
        super().__init__(self.message)

class DatabaseError(RagServiceError):
    """Raised for errors related to database operations (e.g., Neon)."""
    def __init__(self, message="A database error occurred.", original_exception=None):
        self.original_exception = original_exception
        super().__init__(f"{message}: {original_exception}")

class VectorDBError(RagServiceError):
    """Raised for errors related to vector database operations (e.g., Qdrant)."""
    def __init__(self, message="A vector database error occurred.", original_exception=None):
        self.original_exception = original_exception
        super().__init__(f"{message}: {original_exception}")

# --- Decorators for Error Handling and Logging ---

def _log_error(error_type, func, args, kwargs, exc):
    """Helper function to log detailed error information."""
    timestamp = datetime.utcnow().isoformat()
    # Attempt to find session_id or other relevant context from arguments
    session_id = kwargs.get('session_id') or (args[0] if args else 'N/A')
    
    error_log_message = (
        f"Error Type: {error_type}, "
        f"Timestamp: {timestamp}, "
        f"Function: {func.__name__}, "
        f"SessionID: {session_id}, "
        f"Arguments: {args}, "
        f"Keyword Arguments: {kwargs}, "
        f"Exception: {exc}"
    )
    logger.error(error_log_message)

def handle_db_errors(func):
    """
    A decorator to wrap database operations with try/except blocks.
    It logs detailed errors and raises a custom DatabaseError.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Avoid wrapping our own custom exceptions
            if isinstance(e, RagServiceError):
                raise
            
            _log_error("Database", func, args, kwargs, e)
            raise DatabaseError(original_exception=e) from e
    return wrapper

def handle_qdrant_errors(func):
    """
    A decorator to wrap Qdrant operations with try/except blocks.
    It logs detailed errors and raises a custom VectorDBError.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Avoid wrapping our own custom exceptions
            if isinstance(e, RagServiceError):
                raise

            _log_error("VectorDB (Qdrant)", func, args, kwargs, e)
            raise VectorDBError(original_exception=e) from e
    return wrapper

# --- Example of how to use the decorators ---

# This is for demonstration. In a real application, these functions would be elsewhere.

@handle_db_errors
def example_db_function(session_id: str, query: str):
    """Example function that might interact with a database."""
    # Simulate a database failure
    if "fail" in query:
        raise psycopg2.Error("Simulated DB connection failure")
    print(f"Executing query for session {session_id}: {query}")
    return {"result": "data"}

@handle_qdrant_errors
def example_qdrant_function(session_id: str, vector: list):
    """Example function that might interact with Qdrant."""
    # Simulate a Qdrant failure
    if not vector:
        raise Exception("Simulated Qdrant client error: Empty vector")
    print(f"Searching in Qdrant for session {session_id}")
    return {"result": "vector_match"}

if __name__ == '__main__':
    print("--- Testing Database Error Handling ---")
    try:
        example_db_function("session-123", query="SELECT * FROM users")
        example_db_function("session-123", query="fail")
    except DatabaseError as e:
        print(f"Caught expected DatabaseError: {e}")

    print("\n--- Testing Qdrant Error Handling ---")
    try:
        example_qdrant_function("session-456", vector=[0.1, 0.2, 0.3])
        example_qdrant_function("session-456", vector=[])
    except VectorDBError as e:
        print(f"Caught expected VectorDBError: {e}")

    print("\nCheck 'error.log' for detailed error logs.")
