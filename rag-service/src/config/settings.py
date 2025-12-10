from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore') # .env file support, ignore extra fields

    # LLM Configuration
    LLM_API_KEY: str = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Default placeholder
    LLM_MODEL: str = "gemini-pro"
    LLM_TEMPERATURE: float = 0.2
    LLM_BASE_URL: Optional[str] = None # For custom LLM endpoints like OpenRouter

    # Neon (Postgres) Configuration
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "dbname"
    NEON_CONNECTION_TIMEOUT: float = 5.0 # seconds

    @property
    def NEON_DATABASE_URL(self) -> str:
        # Pydantic-settings often needs the full URL or individual components.
        # Construct it here from individual components.
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Qdrant Configuration
    QDRANT_HOST: str = "host.docker.internal"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "humanoid_robotics_chunks"
    QDRANT_SEARCH_TIMEOUT: float = 5.0 # seconds

    # Rate Limiting Configuration (from T047)
    RATE_LIMIT_MAX_REQUESTS: int = 5
    RATE_LIMIT_TIME_WINDOW_SECONDS: int = 60

    # Hallucination Guard Configuration (from T044)
    CONFIDENCE_THRESHOLD: float = 0.7

    # Other settings can be added here
    APP_TITLE: str = "RAG Chatbot Service"
    APP_DESCRIPTION: str = "API for the Retrieval-Augmented Generation (RAG) Chatbot service."
    APP_VERSION: str = "1.0.0"

settings = Settings()

if __name__ == "__main__":
    # Example of how to access settings
    print(f"LLM Model: {settings.LLM_MODEL}")
    print(f"Neon DB URL: {settings.NEON_DATABASE_URL}")
    print(f"Qdrant Host: {settings.QDRANT_HOST}")
    print(f"Rate Limit: {settings.RATE_LIMIT_MAX_REQUESTS} req/{settings.RATE_LIMIT_TIME_WINDOW_SECONDS}s")
    print(f"Confidence Threshold: {settings.CONFIDENCE_THRESHOLD}")

    # You can override settings with environment variables
    # For example, set LLM_MODEL="gemini-flash" in your shell or .env
    # and re-run this script.
