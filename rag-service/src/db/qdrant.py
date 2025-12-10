import os
from qdrant_client import QdrantClient
from ..config.settings import settings # Import settings from the centralized config

def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client instance.
    Connection settings are loaded from the centralized config.
    """
    if not settings.QDRANT_URL:
        raise ValueError("QDRANT_URL is not set in configuration.")

    try:
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        print("Successfully initialized Qdrant client.")
        return client
    except Exception as e:
        print(f"Error initializing Qdrant client: {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    try:
        qdrant_client = get_qdrant_client()
        print(f"Qdrant client: {qdrant_client}")
        # Further operations like qdrant_client.get_collections() can be added here
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")