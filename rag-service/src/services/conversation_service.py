# rag-service/src/services/conversation_service.py

import logging
from typing import List, Dict, Any, Tuple
from ..db.neon_client import get_neondb_connection, close_neondb_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _execute_query(query: str, params: tuple = (), fetch: str = None):
    """
    Executes a given SQL query with parameters and returns the result.
    Handles connection management and basic error logging.
    """
    conn = None
    try:
        conn = get_neondb_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        
        if fetch == 'one':
            result = cursor.fetchone()
            return result
        elif fetch == 'all':
            result = cursor.fetchall()
            return result
        
        cursor.close()
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        # In a real app, you might want to raise a custom exception here
        raise
    finally:
        if conn:
            close_neondb_connection(conn)

def initialize_database():
    """
    Creates the necessary tables if they don't exist.
    """
    logging.info("Initializing database tables...")
    
    # Table for storing conversation messages
    create_conversations_table = """
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL,
        content TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    # Table for storing conversation metadata
    create_metadata_table = """
    CREATE TABLE IF NOT EXISTS conversation_metadata (
        session_id VARCHAR(255) PRIMARY KEY,
        metadata JSONB,
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    _execute_query(create_conversations_table)
    _execute_query(create_metadata_table)
    logging.info("Database tables 'conversations' and 'conversation_metadata' are ready.")

def save_message(session_id: str, role: str, content: str):
    """
    Saves a message to the conversation history.

    Args:
        session_id (str): The unique identifier for the conversation session.
        role (str): The role of the message sender (e.g., 'user', 'assistant').
        content (str): The message content.
    """
    logging.info(f"Saving message for session {session_id}")
    query = "INSERT INTO conversations (session_id, role, content) VALUES (%s, %s, %s)"
    _execute_query(query, (session_id, role, content))

def get_conversation(session_id: str) -> List[Tuple[str, str, str]]:
    """
    Retrieves the entire conversation for a given session ID.

    Args:
        session_id (str): The session identifier.

    Returns:
        A list of tuples, where each tuple contains (role, content, created_at).
    """
    logging.info(f"Retrieving conversation for session {session_id}")
    query = "SELECT role, content, created_at FROM conversations WHERE session_id = %s ORDER BY created_at ASC"
    return _execute_query(query, (session_id,), fetch='all')

def update_metadata(session_id: str, metadata: Dict[str, Any]):
    """
    Saves or updates the metadata for a conversation session.

    Args:
        session_id (str): The session identifier.
        metadata (dict): A dictionary containing metadata.
    """
    import json
    logging.info(f"Updating metadata for session {session_id}")
    # Using INSERT ... ON CONFLICT to handle both new and existing sessions
    query = """
    INSERT INTO conversation_metadata (session_id, metadata)
    VALUES (%s, %s)
    ON CONFLICT (session_id) DO UPDATE 
    SET metadata = conversation_metadata.metadata || EXCLUDED.metadata, updated_at = NOW();
    """
    _execute_query(query, (session_id, json.dumps(metadata)))

def get_metadata(session_id: str) -> Dict[str, Any]:
    """
    Retrieves the metadata for a given session ID.

    Args:
        session_id (str): The session identifier.

    Returns:
        A dictionary containing the metadata.
    """
    logging.info(f"Retrieving metadata for session {session_id}")
    query = "SELECT metadata FROM conversation_metadata WHERE session_id = %s"
    result = _execute_query(query, (session_id,), fetch='one')
    return result[0] if result else None

# Example of initializing the database when the module is loaded
initialize_database()
