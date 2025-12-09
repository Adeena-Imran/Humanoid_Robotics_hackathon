from typing import List
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from ..db.qdrant import get_qdrant_client, QDRANT_COLLECTION_NAME
from ..ingestion.embedder import get_embedding
from ..ingestion.schema import ContentChunk

async def semantic_search(query: str, top_k: int = 5) -> List[ContentChunk]:
    """
    Performs a semantic search in Qdrant for relevant content chunks based on the query.
    """
    client = get_qdrant_client()
    
    # 1. Generate embedding for the query
    query_embedding = get_embedding(query)

    # 2. Perform semantic search in Qdrant
    try:
        search_result = client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k,
            # For filtering by metadata, e.g., to only search a specific chapter:
            # query_filter=Filter(
            #     must=[
            #         FieldCondition(
            #             key="chapter_title",
            #             match=MatchValue(value="Introduction to Humanoid Robotics")
            #         )
            #     ]
            # )
        )
        
        # 3. Convert search results back to ContentChunk objects
        retrieved_chunks: List[ContentChunk] = []
        for hit in search_result:
            payload = hit.payload
            # Ensure embedding is not none for ContentChunk
            if hit.vector is None:
                print(f"Warning: Retrieved chunk {hit.id} has no vector.")
                continue
            
            # Reconstruct ContentChunk from payload and vector
            chunk = ContentChunk(
                chunk_id=payload.get("chunk_id", str(hit.id)), # Use hit.id if chunk_id not in payload
                source_file=payload.get("source_file", "unknown"),
                chapter_title=payload.get("chapter_title", "unknown"),
                section_title=payload.get("section_title"),
                content=payload.get("content", ""),
                embedding=hit.vector # Qdrant returns the vector if `with_vectors=True` (default)
            )
            retrieved_chunks.append(chunk)
            
        return retrieved_chunks
    except Exception as e:
        print(f"Error during semantic search in Qdrant: {e}")
        raise

if __name__ == "__main__":
    # Example usage (requires Qdrant running, config.py settings, and content ingested)
    # This example requires an actual Qdrant instance with data.
    # from ..config import settings
    # if not settings.QDRANT_URL or not settings.OPENAI_API_KEY:
    #     print("QDRANT_URL and OPENAI_API_KEY must be set to run this example.")
    # else:
    #     async def test_semantic_search():
    #         print("Testing semantic search:")
    #         query = "what are the main components of a robot?"
    #         results = await semantic_search(query, top_k=2)
    #         if results:
    #             for i, chunk in enumerate(results):
    #                 print(f"\n--- Result {i+1} (Score: {chunk.score if hasattr(chunk, 'score') else 'N/A'}) ---")
    #                 print(f"Content: {chunk.content[:200]}...")
    #                 print(f"Source: {chunk.source_file}, Chapter: {chunk.chapter_title}")
    #         else:
    #             print("No results found.")

    #     import asyncio
    #     asyncio.run(test_semantic_search())
    pass
