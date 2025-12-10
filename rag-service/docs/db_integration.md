# Neon and Qdrant Integration Guide

This document outlines how to set up and use the Neon and Qdrant integration within the RAG service. Neon is used for persistent storage of conversation histories, while Qdrant is used for efficient vector similarity search on message embeddings.

## 1. Setup Instructions

### Environment Variables

The service requires the following environment variables to connect to Neon and Qdrant. Create a `.env` file in the `rag-service` directory by copying the `.env.example` file and filling in the values.

```bash
# .env file in the rag-service/ directory

# Your Neon Postgres connection string
NEON_DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<dbname>"

# Your Qdrant instance details
QDRANT_HOST="your-qdrant-host"
QDRANT_API_KEY="your-qdrant-api-key" # Optional, if required
```

### Dependencies

All required Python packages are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

## 2. Database Schema

The first time the service runs, it will automatically create two tables in your Neon database if they don't already exist.

### `conversations`

This table stores every message from every conversation.

| Column | Type | Description | 
| :--- | :--- | :--- |
| `id` | SERIAL PRIMARY KEY | Unique identifier for each message. |
| `session_id` | VARCHAR(255) | The identifier for the conversation session. |
| `role` | VARCHAR(50) | The sender of the message (e.g., 'user', 'assistant'). |
| `content` | TEXT | The text of the message. |
| `created_at`| TIMESTAMPTZ | The timestamp when the message was saved. |

### `conversation_metadata`

This table stores metadata associated with each conversation session.

| Column | Type | Description | 
| :--- | :--- | :--- |
| `session_id` | VARCHAR(255) PRIMARY KEY| The unique session identifier, linking to the `conversations` table. |
| `metadata` | JSONB | A flexible JSON object to store metadata (e.g., user ID, topic). |
| `updated_at`| TIMESTAMPTZ | The timestamp when the metadata was last updated. |

## 3. Usage Examples

To interact with the conversation history, use the helper functions provided in `src.services.neon_helpers`. These functions include built-in error handling.

```python
from src.services import neon_helpers
from src.utils.error_handling import DatabaseError

SESSION_ID = "my-test-session-001"

try:
    # Save messages to the database
    print("Saving messages...")
    neon_helpers.save_message(SESSION_ID, "user", "How does a transformer model work?")
    neon_helpers.save_message(SESSION_ID, "assistant", "It uses an attention mechanism to weigh the importance of different words in the input sequence.")
    print("Messages saved.")

    # Retrieve the conversation
    print("\nRetrieving conversation...")
    history = neon_helpers.get_conversation(SESSION_ID)
    for role, content, ts in history:
        print(f"- [{ts}] {role}: {content}")

    # Update metadata
    print("\nUpdating metadata...")
    metadata = {"user_id": "user-xyz", "model_used": "GPT-4"}
    neon_helpers.update_metadata(SESSION_ID, metadata)
    print("Metadata updated.")
    
    # Retrieve metadata
    retrieved_meta = neon_helpers.get_metadata(SESSION_ID)
    print(f"Retrieved metadata: {retrieved_meta}")

except DatabaseError as e:
    print(f"An error occurred: {e}")

```

## 4. Testing the Integration

An end-to-end integration test is available to verify that both Neon and Qdrant are working correctly.

To run the tests, ensure your `.env` file is configured with credentials for a **test database and test Qdrant instance**, as the tests will create and delete data.

Execute the tests from the root of the project directory using the following command:

```bash
python -m unittest discover -s rag-service/tests
```

The test script will:
1. Create temporary tables and collections.
2. Save mock conversation data to Neon.
3. Store mock vector embeddings in Qdrant.
4. Retrieve the data from both services and assert that it is correct.
5. Clean up all test data and collections.

```