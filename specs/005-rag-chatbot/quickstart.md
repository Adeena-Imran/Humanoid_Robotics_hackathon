# Quickstart: RAG Chatbot Service (FastAPI)

This guide provides instructions to quickly set up and run the FastAPI-based RAG Chatbot service.

## 1. Prerequisites

*   Python 3.9+
*   `pip` (Python package installer)
*   `git`
*   Access to:
    *   Qdrant Cloud (or local Qdrant instance)
    *   Neon Serverless Postgres database
    *   OpenAI API key (or access to compatible LLM API)

## 2. Setup Project

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd humanoid_robotics_book
    ```
2.  **Navigate to the RAG Service directory:**
    ```bash
    mkdir rag-service
    cd rag-service
    ```
    *(Note: This directory will contain the FastAPI application.)*

3.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source ./.venv/bin/activate
    ```

4.  **Install dependencies:**
    *(Note: The `requirements.txt` file will be created during implementation.)*
    ```bash
    pip install "fastapi[all]" uvicorn python-dotenv qdrant-client psycopg2-binary openai tiktoken
    ```
    (This list is an initial suggestion and might be updated during implementation.)

5.  **Configure environment variables:**
    Create a `.env` file in the `rag-service/` directory with the following variables:
    ```dotenv
    OPENAI_API_KEY="your_openai_api_key"
    QDRANT_URL="your_qdrant_cloud_url"
    QDRANT_API_KEY="your_qdrant_api_key"
    NEON_POSTGRES_URL="your_neon_postgres_connection_string"
    ```

## 3. Initial Data Ingestion (Conceptual)

*(Note: An ingestion script will be developed to process book content.)*

Before running the chatbot, you need to ingest the book content into Qdrant and Neon Postgres.
1.  **Ensure book content is available:** The Markdown/MDX files are expected to be in `my-textbook-site/docs/`.
2.  **Run the ingestion script:**
    ```bash
    # This command is illustrative; actual command will be defined during implementation
    python scripts/ingest_book_content.py --docs-path ../my-textbook-site/docs
    ```
    This script will:
    *   Parse `.mdx` files into `Content Chunks`.
    *   Generate embeddings for each chunk.
    *   Store embeddings and metadata in Qdrant.
    *   Store chapter summaries and other metadata in Neon Postgres.

## 4. Run the FastAPI Service

1.  **Ensure virtual environment is active.**
2.  **Start the Uvicorn server:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    (Assuming your main FastAPI application file is `main.py` and the FastAPI app instance is named `app`.)

3.  **Access the API:**
    *   **Swagger UI:** Open your browser and navigate to `http://localhost:8000/docs` to interact with the API via Swagger UI.
    *   **Redoc UI:** Open your browser and navigate to `http://localhost:8000/redoc` for Redoc documentation.

## 5. Testing

*(Note: Tests will be located in the `rag-service/tests/` directory.)*

Run tests using `pytest`:
```bash
pytest
```
