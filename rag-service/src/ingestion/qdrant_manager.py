from typing import List
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from ..db.qdrant import get_qdrant_client
from ..ingestion.schema import ContentChunk

QDRANT_COLLECTION_NAME = "book_content" # Default collection name

def create_qdrant_collection(
    collection_name: str = QDRANT_COLLECTION_NAME,
    vector_size: int = 1536, # OpenAI's text-embedding-ada-002 size
    distance: Distance = Distance.COSINE
):
    """
    Creates a Qdrant collection if it does not already exist.
    """
    client = get_qdrant_client()
    try:
        if not client.collection_exists(collection_name=collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Error creating Qdrant collection '{collection_name}': {e}")
        raise

def upsert_chunks_to_qdrant(
    chunks: List[ContentChunk],
    collection_name: str = QDRANT_COLLECTION_NAME,
):
    """
    Upserts a list of ContentChunk objects to the specified Qdrant collection.
    """
    if not chunks:
        print("No chunks to upsert.")
        return

    client = get_qdrant_client()
    points = []
    for chunk in chunks:
        # Prepare payload from ContentChunk (excluding embedding and chunk_id)
        payload = chunk.model_dump(exclude={'embedding'})
        points.append(
            PointStruct(
                id=hash(chunk.chunk_id), # Qdrant expects int or UUID for point ID
                vector=chunk.embedding,
                payload=payload
            )
        )
    
    try:
        # Use batch upsert for efficiency
        client.upsert(
            collection_name=collection_name,
            wait=True,
            points=points
        )
        print(f"Upserted {len(chunks)} chunks to collection '{collection_name}'.")
    except Exception as e:
        print(f"Error upserting chunks to Qdrant collection '{collection_name}': {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    # This requires Qdrant to be running and config.py settings to be correct
    # and schema.py to be importable
    try:
        # Create a dummy collection (e.g., "test_collection")
        test_collection_name = "test_book_content"
        create_qdrant_collection(collection_name=test_collection_name)

        # Create dummy chunks (need embeddings for real usage)
        from ..config import settings
        if not settings.OPENAI_API_KEY:
             print("OPENAI_API_KEY not set. Cannot generate real embeddings for test.")
             dummy_embedding = [0.0] * 1536
        else:
            from ..ingestion.embedder import get_embedding
            dummy_embedding = get_embedding("This is a dummy chunk for testing Qdrant manager.")

        dummy_chunks = [
            ContentChunk(
                chunk_id="test-chunk-1",
                source_file="test_file.mdx",
                chapter_title="Test Chapter",
                section_title="Test Section 1",
                content="This is the content of test chunk 1.",
                embedding=dummy_embedding
            ),
            ContentChunk(
                chunk_id="test-chunk-2",
                source_file="test_file.mdx",
                chapter_title="Test Chapter",
                section_title="Test Section 2",
                content="This is the content of test chunk 2.",
                embedding=dummy_embedding
            )
        ]
        upsert_chunks_to_qdrant(dummy_chunks, collection_name=test_collection_name)

        # Clean up (optional)
        # get_qdrant_client().delete_collection(collection_name=test_collection_name)
        # print(f"Collection '{test_collection_name}' deleted.")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during Qdrant manager example: {e}")
