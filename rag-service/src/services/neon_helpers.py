# rag-service/src/services/neon_helpers.py

from typing import Dict, Any, List, Tuple
from . import conversation_service
from ..utils.error_handling import handle_db_errors, DatabaseError

@handle_db_errors
def get_conversation(session_id: str) -> List[Tuple[str, str, str]]:
    """
    A helper function to safely retrieve a conversation history.

    This function reuses the `get_conversation` logic from the conversation_service
    and wraps it with standardized error handling.

    Args:
        session_id (str): The unique identifier for the conversation.

    Returns:
        A list of tuples, each containing (role, content, created_at).

    Raises:
        DatabaseError: If any database-related error occurs.
    """
    return conversation_service.get_conversation(session_id=session_id)

@handle_db_errors
def save_message(session_id: str, role: str, content: str):
    """
    A helper function to safely save a message to the conversation history.

    This function reuses the `save_message` logic from the conversation_service
    and wraps it with standardized error handling.

    Args:
        session_id (str): The unique identifier for the conversation.
        role (str): The role of the message sender (e.g., 'user', 'assistant').
        content (str): The message content.

    Raises:
        DatabaseError: If any database-related error occurs.
    """
    conversation_service.save_message(session_id=session_id, role=role, content=content)

@handle_db_errors
def update_metadata(session_id: str, data: Dict[str, Any]):
    """
    A helper function to safely update conversation metadata.

    This function reuses the `update_metadata` logic from the conversation_service
    and wraps it with standardized error handling.

    Args:
        session_id (str): The unique identifier for the conversation.
        data (Dict[str, Any]): A dictionary containing the metadata to save or update.

    Raises:
        DatabaseError: If any database-related error occurs.
    """
    conversation_service.update_metadata(session_id=session_id, metadata=data)

@handle_db_errors
def get_metadata(session_id: str) -> Dict[str, Any]:
    """
    A helper function to safely retrieve conversation metadata.

    This function reuses the `get_metadata` logic from the conversation_service
    and wraps it with standardized error handling.

    Args:
        session_id (str): The unique identifier for the conversation.

    Returns:
        A dictionary containing the metadata.

    Raises:
        DatabaseError: If any database-related error occurs.
    """
    return conversation_service.get_metadata(session_id=session_id)


# Example Usage (for demonstration purposes)
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv() # Load environment variables for direct execution

    # This assumes your NEON_DATABASE_URL is set correctly in your environment
    
    TEST_SESSION_ID = "test-helper-session-001"
    
    print(f"--- Testing Neon Helpers for Session: {TEST_SESSION_ID} ---")
    
    # Initialize DB (creates tables if they don't exist)
    try:
        conversation_service.initialize_database()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization failed. Ensure NEON_DATABASE_URL is set. Error: {e}")
        exit(1)

    # 1. Save messages
    try:
        print("\n1. Saving messages...")
        save_message(TEST_SESSION_ID, "user", "Hello, what is reinforcement learning?")
        save_message(TEST_SESSION_ID, "assistant", "Reinforcement learning is a type of machine learning...")
        print("   ...Messages saved successfully.")
    except DatabaseError as e:
        print(f"   ...Failed to save messages: {e}")

    # 2. Retrieve conversation
    try:
        print("\n2. Retrieving conversation...")
        history = get_conversation(TEST_SESSION_ID)
        if history:
            print("   ...Conversation retrieved successfully:")
            for role, content, timestamp in history:
                print(f"     - [{timestamp}] {role.title()}: {content[:50]}...")
        else:
            print("   ...No conversation found.")
    except DatabaseError as e:
        print(f"   ...Failed to retrieve conversation: {e}")
        
    # 3. Update metadata
    try:
        print("\n3. Updating metadata...")
        metadata_to_add = {"user_id": "user-abc-123", "topic": "ML"}
        update_metadata(TEST_SESSION_ID, metadata_to_add)
        print(f"   ...Metadata updated successfully with: {metadata_to_add}")
        
        # Update again to test merging
        more_metadata = {"status": "active", "user_rating": 5}
        update_metadata(TEST_SESSION_ID, more_metadata)
        print(f"   ...Merged metadata with: {more_metadata}")
        
    except DatabaseError as e:
        print(f"   ...Failed to update metadata: {e}")

    print("\n--- Test Complete ---")
