import asyncio
import logging
from functools import wraps
from typing import Callable, Awaitable, Tuple, Type, Union

logger = logging.getLogger(__name__)

# Define common transient exceptions. This list can be expanded.
# For a real application, you'd tailor this to Neon/Qdrant specific transient errors.
TRANSIENT_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    asyncio.TimeoutError, # Generic timeout
    ConnectionError,      # Base class for connection-related issues
    OSError,              # OS-related errors (e.g., connection reset by peer)
    # Add specific Neon/Qdrant client exceptions here as they become known
    # e.g., qdrant_client.http.exceptions.UnexpectedResponse,
    #       asyncpg.exceptions.ConnectionDoesNotExistError,
)

def retry(
    max_retries: int = 3,
    initial_delay_seconds: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions_to_retry: Union[Tuple[Type[Exception], ...], None] = None,
) -> Callable:
    """
    A generic asynchronous retry decorator for external service calls.

    Args:
        max_retries: The maximum number of times to retry the operation.
        initial_delay_seconds: The initial delay before the first retry.
        backoff_factor: The factor by which the delay increases with each retry.
                        (delay = initial_delay_seconds * (backoff_factor ** (retry_num - 1)))
        exceptions_to_retry: A tuple of exception types that should trigger a retry.
                             If None, TRANSIENT_EXCEPTIONS will be used.
    """
    if exceptions_to_retry is None:
        exceptions_to_retry = TRANSIENT_EXCEPTIONS

    def decorator(func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay_seconds
            for i in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions_to_retry as e:
                    if i == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries + 1} attempts due to {type(e).__name__}: {e}")
                        raise  # Re-raise the exception after exhausting retries
                    
                    logger.warning(f"Function {func.__name__} failed due to {type(e).__name__}: {e}. Retrying in {delay:.2f} seconds (attempt {i+1}/{max_retries})...")
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
                except Exception as e:
                    # Catch any other unexpected exceptions and re-raise immediately
                    logger.error(f"Function {func.__name__} encountered an unexpected error {type(e).__name__}: {e}. Not retrying.")
                    raise
        return wrapper
    return decorator

# Example usage for demonstration
async def flaky_function(attempt: int, fail_until_attempt: int):
    print(f"  Attempt {attempt} - Running flaky_function...")
    if attempt < fail_until_attempt:
        if attempt % 2 == 0:
            raise ConnectionError("Simulated connection error")
        else:
            raise asyncio.TimeoutError("Simulated timeout error")
    print(f"  Attempt {attempt} - flaky_function succeeded!")
    return f"Success at attempt {attempt}"

async def main():
    @retry(max_retries=2, initial_delay_seconds=0.1, backoff_factor=2)
    async def reliable_flaky_func(fail_until: int):
        current_attempt = 1
        while True: # Simulate the function making attempts
            try:
                return await flaky_function(current_attempt, fail_until)
            except (ConnectionError, asyncio.TimeoutError) as e:
                current_attempt += 1
                # In a real retry decorator, this logic would be inside the decorator.
                # For this example, we manually increment attempt to control `flaky_function`
                raise e # Re-raise for the decorator to catch

    print("---"Test Case 1: Succeeds after retries ---")
    try:
        result = await reliable_flaky_func(fail_until=2) # Fails 1st, succeeds 2nd
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Unexpected error: {e}\n")

    print("---"Test Case 2: Fails after exhausting retries ---")
    try:
        result = await reliable_flaky_func(fail_until=4) # Fails 1st, 2nd, 3rd (max_retries=2), then gives up
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Expected error after retries: {type(e).__name__}: {e}\n")

    @retry(max_retries=1, exceptions_to_retry=(ValueError,))
    async def func_with_specific_retry():
        print("  Running func_with_specific_retry...")
        raise ValueError("Specific error to retry")

    print("---"Test Case 3: Fails on non-configured exception ---")
    try:
        @retry(max_retries=1) # Default exceptions
        async def func_unexpected_error():
            print("  Running func_unexpected_error...")
            raise ValueError("An unexpected error type")
        await func_unexpected_error()
    except Exception as e:
        print(f"Expected immediate error: {type(e).__name__}: {e}\n")

if __name__ == "__main__":
    # Setup basic logging to see retry messages
    logging.basicConfig(level=logging.INFO) 
    asyncio.run(main())
