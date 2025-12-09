from typing import List
from openai import OpenAI
from ..config import settings

def get_embedding(text: str) -> List[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding model.
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in configuration.")

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(
            model="text-embedding-ada-002", # Or a newer suitable model
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    # Set OPENAI_API_KEY in your .env file or environment variables for this to work
    try:
        sample_text = "This is a test sentence for embedding."
        embedding = get_embedding(sample_text)
        print(f"Embedding length: {len(embedding)}")
        print(f"First 5 elements of embedding: {embedding[:5]}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}. Make sure your OPENAI_API_KEY is set and valid.")
