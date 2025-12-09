import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Centralized configuration for the RAG service, loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    QDRANT_URL: str
    QDRANT_API_KEY: str | None = None  # Optional API key for Qdrant

    POSTGRES_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Add other settings here as needed, e.g., LLM specific settings
    OPENAI_API_KEY: str | None = None


# Instantiate settings to be imported by other modules
settings = Settings()

if __name__ == "__main__":
    # Example usage:
    print("RAG Service Configuration:")
    print(f"Qdrant URL: {settings.QDRANT_URL}")
    print(f"Qdrant API Key (set): {'Yes' if settings.QDRANT_API_KEY else 'No'}")
    print(f"Postgres URL: {settings.POSTGRES_URL}")
    print(f"Postgres User: {settings.POSTGRES_USER}")
    print(f"Postgres DB: {settings.POSTGRES_DB}")
    print(f"OpenAI API Key (set): {'Yes' if settings.OPENAI_API_KEY else 'No'}")

    # Test for missing mandatory variables
    try:
        # Temporarily unset a mandatory variable to test error handling
        original_qdrant_url = os.getenv("QDRANT_URL")
        del os.environ["QDRANT_URL"]
        Settings() # This should raise a ValidationError
    except Exception as e:
        print(f"\nExpected error for missing QDRANT_URL: {e}")
    finally:
        if original_qdrant_url:
            os.environ["QDRANT_URL"] = original_qdrant_url
