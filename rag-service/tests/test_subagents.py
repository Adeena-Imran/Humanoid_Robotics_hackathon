import pytest
import asyncio
from unittest.mock import AsyncMock, patch

# Import the services to be tested
from rag-service.src.services.subagent_service import SubagentService
from rag-service.src.services.skill_service import SkillService, execute_placeholder_skill
from rag-service.src.services.context_service import ContextService

# Mock global stores for the mock DB functions
# This is how the mock DB functions in the services interact
_mock_subagents_store = {}
_mock_skill_logs_store = []
_mock_context_store = {}

@pytest.fixture(autouse=True)
def setup_mock_stores():
    """Reset mock stores before each test."""
    global _mock_subagents_store, _mock_skill_logs_store, _mock_context_store
    _mock_subagents_store = {}
    _mock_skill_logs_store = []
    _mock_context_store = {}

# Patch the mock DB functions used by the services
@pytest.fixture(autouse=True)
def mock_db_functions():
    with patch('rag-service.src.services.subagent_service.get_db_connection', new_callable=AsyncMock) as mock_subagent_get_db_connection, \
         patch('rag-service.src.services.subagent_service.store_metadata', new_callable=AsyncMock) as mock_subagent_store_metadata, \
         patch('rag-service.src.services.subagent_service.get_metadata', new_callable=AsyncMock) as mock_subagent_get_metadata, \
         patch('rag-service.src.services.subagent_service.list_metadata_keys', new_callable=AsyncMock) as mock_subagent_list_metadata_keys, \
         patch('rag-service.src.services.skill_service.get_db_connection', new_callable=AsyncMock) as mock_skill_get_db_connection, \
         patch('rag-service.src.services.skill_service.store_skill_log', new_callable=AsyncMock) as mock_skill_store_skill_log, \
         patch('rag-service.src.services.context_service.get_db_connection', new_callable=AsyncMock) as mock_context_get_db_connection, \
         patch('rag-service.src.services.context_service.store_metadata', new_callable=AsyncMock) as mock_context_store_metadata, \
         patch('rag-service.src.services.context_service.get_metadata', new_callable=AsyncMock) as mock_context_get_metadata:

        # Mock implementations for subagent_service
        mock_subagent_get_db_connection.return_value = "mock_conn_subagent"
        mock_subagent_store_metadata.side_effect = lambda conn, key, data: _mock_subagents_store.update({key: data})
        mock_subagent_get_metadata.side_effect = lambda conn, key: _mock_subagents_store.get(key)
        mock_subagent_list_metadata_keys.side_effect = lambda conn, prefix: [k for k in _mock_subagents_store.keys() if k.startswith(prefix)]

        # Mock implementations for skill_service
        mock_skill_get_db_connection.return_value = "mock_conn_skill"
        mock_skill_store_skill_log.side_effect = lambda conn, log_entry: _mock_skill_logs_store.append(log_entry)

        # Mock implementations for context_service
        mock_context_get_db_connection.return_value = "mock_conn_context"
        mock_context_store_metadata.side_effect = lambda conn, key, data: _mock_context_store.update({key: data})
        mock_context_get_metadata.side_effect = lambda conn, key: _mock_context_store.get(key)
        
        yield # Allow the tests to run

@pytest.mark.asyncio
async def test_subagent_creation_and_retrieval():
    """
    Validate subagent creation and retrieval using SubagentService.
    """
    subagent_service = SubagentService()

    # Create two sample subagents
    await subagent_service.create_subagent("researcher", "Performs research.")
    await subagent_service.create_subagent("writer", "Writes content.")

    # Retrieve and assert
    researcher = await subagent_service.get_subagent("researcher")
    assert researcher is not None
    assert researcher["name"] == "researcher"
    assert researcher["purpose"] == "Performs research."

    writer = await subagent_service.get_subagent("writer")
    assert writer is not None
    assert writer["name"] == "writer"
    assert writer["purpose"] == "Writes content."

    # List subagents
    all_subagents = await subagent_service.list_subagents()
    assert len(all_subagents) == 2
    assert any(sa["name"] == "researcher" for sa in all_subagents)
    assert any(sa["name"] == "writer" for sa in all_subagents)

    # Test for non-existent subagent
    non_existent = await subagent_service.get_subagent("editor")
    assert non_existent is None

    # Test duplicate creation
    with pytest.raises(ValueError, match="Subagent with name 'researcher' already exists."):
        await subagent_service.create_subagent("researcher", "Another purpose.")

@pytest.mark.asyncio
async def test_skill_chaining():
    """
    Validate skill chaining logic using SkillService.
    """
    skill_service = SkillService()

    # Define mock skills for the chain
    mock_skills = [
        {"name": "step1"},
        {"name": "step2"},
        {"name": "step3"},
    ]
    initial_input = {"start": "data"}

    # Execute the skill chain
    result = await skill_service.execute_skill_chain("test_subagent", mock_skills, initial_input)

    # Assert final output format
    assert "final_output" in result
    assert "execution_log" in result
    assert isinstance(result["final_output"], str)
    assert "Output from step3 after processing: Output from step2 after processing: Output from step1 after processing: {'start': 'data'}" in result["final_output"]

    # Assert log entries
    assert len(_mock_skill_logs_store) == 6 # 3 skills * (started + completed)
    
    # Check a started log entry
    step1_start_log = next(log for log in _mock_skill_logs_store if log["skill_name"] == "step1" and log["status"] == "started")
    assert step1_start_log["input"] == initial_input

    # Check a completed log entry
    step2_completed_log = next(log for log in _mock_skill_logs_store if log["skill_name"] == "step2" and log["status"] == "completed")
    assert "Output from step1" in step2_completed_log["input"] # Output of step1 is input of step2
    assert "Output from step2" in step2_completed_log["output"]

@pytest.mark.asyncio
async def test_context_handling():
    """
    Validate context storage and retrieval using ContextService.
    """
    context_service = ContextService()

    subagent_name = "test_agent"
    session_id = "test_session_123"
    context_data = {"last_query": "robotics", "response_count": 5}

    # Save context
    await context_service.save_context(subagent_name, session_id, context_data)

    # Retrieve context
    retrieved_context = await context_service.get_context(subagent_name, session_id)
    assert retrieved_context is not None
    assert retrieved_context == context_data

    # Update context
    updated_context_data = {"last_query": "AI", "response_count": 6, "new_field": True}
    await context_service.save_context(subagent_name, session_id, updated_context_data)
    retrieved_updated_context = await context_service.get_context(subagent_name, session_id)
    assert retrieved_updated_context == updated_context_data

    # Retrieve non-existent context
    non_existent_context = await context_service.get_context("another_agent", "another_session")
    assert non_existent_context is None
