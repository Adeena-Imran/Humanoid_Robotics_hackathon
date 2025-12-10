import asyncio
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint
from ..ingestion.schema import ContentChunk
from ..llm.client import LLMClient
from ..utils.api_errors import InternalServerErrorException
from ..config.settings import settings

class QdrantService:
    """
    Service for interacting with Qdrant for vector search.
    """
    def __init__(self, llm_client: LLMClient):
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.llm_client = llm_client # Used for embedding queries

    async def search_qdrant(self, query_embedding: List[float], limit: int = 5) -> List[ScoredPoint]:
        """
        Performs a vector search in Qdrant with a timeout.
        """
        try:
            # Qdrant client methods are typically blocking, so run in a thread pool
            search_result = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.search,
                    collection_name=settings.QDRANT_COLLECTION_NAME,
                    query_vector=query_embedding,
                    limit=limit
                ),
                timeout=settings.QDRANT_SEARCH_TIMEOUT
            )
            return search_result
        except asyncio.TimeoutError:
            raise InternalServerErrorException(
                code="QDRANT_SEARCH_TIMEOUT",
                message=f"Qdrant search timed out after {settings.QDRANT_SEARCH_TIMEOUT} seconds.",
                target="Qdrant"
            )
        except Exception as e:
            raise InternalServerErrorException(
                code="QDRANT_SEARCH_FAILED",
                message=f"Qdrant search failed: {e}",
                target="Qdrant"
            )

async def semantic_search(query: str, limit: int = 5) -> List[ContentChunk]:
    """
    Performs a semantic search for the given query using Qdrant.
    """
    llm_client = LLMClient() # Initialize LLM client for embedding
    qdrant_service = QdrantService(llm_client)

    # 1. Generate embedding for the query
    query_embedding = await llm_client.get_embedding(query)

    # 2. Search Qdrant
    search_results = await qdrant_service.search_qdrant(query_embedding, limit=limit)

    # 3. Convert search results to ContentChunk (assuming payload contains necessary fields)
    content_chunks: List[ContentChunk] = []
    for scored_point in search_results:
        payload = scored_point.payload
        if payload:
            content_chunks.append(
                ContentChunk(
                    content=payload.get("content", ""),
                    source_file=payload.get("source_file", "unknown"),
                    chapter_title=payload.get("chapter_title", "unknown"),
                    section_title=payload.get("section_title"),
                )
            )
    return content_chunks

# Example usage
async def main():
    print("--- Testing Semantic Search with Timeout ---")
    # Mock LLM client for embedding
    class MockLLMClient:
        async def get_embedding(self, text: str) -> List[float]:
            print(f"Generating mock embedding for: {text}")
            return [0.1] * 1536 # Example embedding

    llm_client_instance = MockLLMClient()
    
    # Patch QdrantClient to mock search results
    with patch('qdrant_client.QdrantClient') as MockQdrantClient:
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_qdrant_instance.search.return_value = [
            ScoredPoint(id=1, version=1, score=0.9, payload={"content": "Mock content 1", "source_file": "doc1.md", "chapter_title": "Ch1"}),
            ScoredPoint(id=2, version=1, score=0.8, payload={"content": "Mock content 2", "source_file": "doc2.md", "chapter_title": "Ch2"})
        ]

        qdrant_service = QdrantService(llm_client_instance)

        try:
            chunks = await qdrant_service.search_qdrant([0.1]*1536)
            print(f"Found {len(chunks)} chunks.")
            for chunk in chunks:
                print(f"- {chunk.content[:20]}... from {chunk.payload.get('source_file')}")
        except InternalServerErrorException as e:
            print(f"Error: {e.to_api_error().model_dump_json(indent=2)}")

    print("\n--- Testing Semantic Search Timeout (simulated) ---")
    original_timeout = settings.QDRANT_SEARCH_TIMEOUT
    # Temporarily override setting for testing purposes
    settings.QDRANT_SEARCH_TIMEOUT = 0.01 
    
    with patch('qdrant_client.QdrantClient') as MockQdrantClient:
        mock_qdrant_instance = MockQdrantClient.return_value
        # Make the search call 'hang' longer than the timeout
        mock_qdrant_instance.search.side_effect = lambda **kwargs: asyncio.sleep(0.1) 

        qdrant_service = QdrantService(llm_client_instance)
        try:
            await qdrant_service.search_qdrant([0.1]*1536)
        except InternalServerErrorException as e:
            print(f"Error: {e.to_api_error().model_dump_json(indent=2)}")
        finally:
            settings.QDRANT_SEARCH_TIMEOUT = original_timeout # Reset setting

if __name__ == "__main__":
    from unittest.mock import patch
    asyncio.run(main())