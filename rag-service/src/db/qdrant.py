import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client instance.
    Connection settings are loaded from environment variables.
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url:
        raise ValueError("QDRANT_URL environment variable is not set.")

    try:
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,  # API key is optional for local/unsecured instances
        )
        # Optional: Test connection
        # client.get_collections()
        print("Successfully connected to Qdrant.")
        return client
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    try:
        qdrant_client = get_qdrant_client()
        # You can perform some operations with the client here, exp:
        # print(qdrant_client.get_collections())
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
