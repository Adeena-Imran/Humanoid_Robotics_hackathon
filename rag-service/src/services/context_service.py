from typing import Dict, Any, Optional
import asyncio

# Assuming the existence of mock DB helpers from subagent_service/skill_service for context storage
# In a real scenario, this would be a proper import or a shared db_utils module.
async def get_db_connection():
    # This is a mock connection.
    print("Connecting to database for context service...")
    await asyncio.sleep(0.05) # Simulate async connection
    return "mock_context_connection"

async def store_metadata(conn: Any, key: str, data: Dict[str, Any]):
    # This is a mock storage function.
    print(f"Storing context metadata for key '{key}': {data}")
    await asyncio.sleep(0.05) # Simulate async write
    if 'context_store' not in globals():
        globals()['context_store'] = {}
    globals()['context_store'][key] = data
    return True

async def get_metadata(conn: Any, key: str) -> Optional[Dict[str, Any]]:
    # This is a mock retrieval function.
    print(f"Retrieving context metadata for key '{key}'")
    await asyncio.sleep(0.05) # Simulate async read
    return globals().get('context_store', {}).get(key)


class ContextService:
    """
    Manages subagent-specific conversational context, storing and retrieving it from Neon.
    """

    async def save_context(self, subagent_name: str, session_id: str, context: Dict[str, Any]):
        """
        Saves the current context for a given subagent and session.

        Args:
            subagent_name: The name of the subagent.
            session_id: The unique identifier for the conversation session.
            context: A dictionary representing the context to be saved.
        """
        if not subagent_name or not session_id or not context:
            raise ValueError("Subagent name, session ID, and context cannot be empty.")

        conn = await get_db_connection()
        context_key = f"context_{subagent_name}_{session_id}"
        await store_metadata(conn, context_key, context)
        print(f"Context for subagent '{subagent_name}', session '{session_id}' saved.")

    async def get_context(self, subagent_name: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the stored context for a given subagent and session.

        Args:
            subagent_name: The name of the subagent.
            session_id: The unique identifier for the conversation session.

        Returns:
            A dictionary with the stored context, or None if no context is found.
        """
        if not subagent_name or not session_id:
            raise ValueError("Subagent name and session ID cannot be empty.")
            
        conn = await get_db_connection()
        context_key = f"context_{subagent_name}_{session_id}"
        context_data = await get_metadata(conn, context_key)

        # IMPORTANT: The requirement states: "Context should be automatically merged with Qdrant retrieval results when available."
        # This merging logic would typically happen at the point where context is *used* for a query,
        # likely within the main /chat endpoint or a dedicated retrieval orchestrator,
        # after Qdrant results have been obtained. For this task, we just retrieve the stored context.
        # The merging implementation is deferred to T039 or a later, more integrated task.
        if context_data:
            print(f"Context for subagent '{subagent_name}', session '{session_id}' retrieved.")
        else:
            print(f"No context found for subagent '{subagent_name}', session '{session_id}'.")
            
        return context_data


# Example usage (for testing purposes)
async def main():
    service = ContextService()

    subagent_name = "researcher_subagent"
    session_id = "user123_conv456"
    initial_context = {"user_preference": "concise answers", "recent_topics": ["robotics", "AI"]}

    print("--- Saving Context ---")
    await service.save_context(subagent_name, session_id, initial_context)

    print("\n--- Retrieving Context ---")
    retrieved_context = await service.get_context(subagent_name, session_id)
    if retrieved_context:
        print(f"Retrieved context: {retrieved_context}")

    print("\n--- Retrieving Non-existent Context ---")
    non_existent_context = await service.get_context("unknown_agent", "unknown_session")
    if not non_existent_context:
        print("Correctly returned None for non-existent context.")

    updated_context = {"user_preference": "detailed answers", "last_query": "humanoid gait"}
    await service.save_context(subagent_name, session_id, updated_context)
    retrieved_updated_context = await service.get_context(subagent_name, session_id)
    if retrieved_updated_context:
        print(f"Retrieved updated context: {retrieved_updated_context}")


if __name__ == "__main__":
    asyncio.run(main())
