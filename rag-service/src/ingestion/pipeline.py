import os
import glob
from typing import List
from ..db.qdrant import get_qdrant_client
from ..db.postgres import get_postgres_connection
from ..ingestion.chunker import chunk_markdown
from ..ingestion.metadata_extractor import extract_and_format_metadata
from ..ingestion.embedder import get_embedding
from ..ingestion.schema import ContentChunk, ChapterSummary
from .qdrant_manager import create_qdrant_collection, upsert_chunks_to_qdrant, QDRANT_COLLECTION_NAME

def read_markdown_files(docs_path: str) -> Dict[str, str]:
    """
    Reads all Markdown/MDX files from the specified documentation path.
    Returns a dictionary mapping file paths to their content.
    """
    file_contents = {}
    for filepath in glob.glob(os.path.join(docs_path, '**/*.md'), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            file_contents[filepath] = f.read()
    for filepath in glob.glob(os.path.join(docs_path, '**/*.mdx'), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            file_contents[filepath] = f.read()
    return file_contents

def ingestion_pipeline(docs_path: str):
    """
    Orchestrates the entire ingestion process:
    1. Reads Markdown/MDX files.
    2. Chunks content and extracts metadata.
    3. Generates embeddings.
    4. Stores chunks and embeddings in Qdrant.
    5. Stores chapter summaries and other metadata in Neon Postgres.
    """
    print(f"Starting ingestion pipeline from: {docs_path}")

    # 1. Read files
    raw_docs = read_markdown_files(docs_path)
    if not raw_docs:
        print(f"No markdown/mdx files found in {docs_path}. Exiting ingestion.")
        return

    all_content_chunks: List[ContentChunk] = []
    
    # Ensure Qdrant collection exists
    create_qdrant_collection(collection_name=QDRANT_COLLECTION_NAME)

    # 2. Process each document
    for file_path, content in raw_docs.items():
        print(f"Processing file: {file_path}")
        # Chunk content
        raw_chunks = chunk_markdown(content, file_path)
        
        # Generate embeddings and format into ContentChunk
        chunks_to_upsert: List[ContentChunk] = []
        for raw_chunk_data in raw_chunks:
            try:
                embedding = get_embedding(raw_chunk_data['content'])
                content_chunk = extract_and_format_metadata(raw_chunk_data, embedding)
                chunks_to_upsert.append(content_chunk)
                all_content_chunks.append(content_chunk)
            except Exception as e:
                print(f"Skipping chunk due to embedding error in {file_path}: {e}")
        
        # Upsert to Qdrant in batches
        if chunks_to_upsert:
            upsert_chunks_to_qdrant(chunks_to_upsert, collection_name=QDRANT_COLLECTION_NAME)

    # 3. Handle Chapter Summaries (conceptual - requires a summarization service)
    # For now, this is a placeholder. Actual summarization logic would go here.
    # We might need to store chapter metadata in Postgres initially.
    
    # Placeholder for Postgres operations:
    try:
        conn = get_postgres_connection()
        if conn:
            with conn.cursor() as cur:
                # Example: Create a table for document metadata if it doesn't exist
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS document_metadata (
                        id SERIAL PRIMARY KEY,
                        file_path TEXT UNIQUE,
                        chapter_title TEXT,
                        last_ingested TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                # Example: Upsert metadata for processed files
                for file_path, content in raw_docs.items():
                    # This needs actual chapter title extraction,
                    # for simplicity using a placeholder
                    chapter_title_for_db = "Unknown Chapter" # Placeholder
                    if all_content_chunks:
                        # Try to get chapter title from one of the chunks
                        # belonging to this file
                        first_chunk_for_file = next((c for c in all_content_chunks if c.source_file == file_path), None)
                        if first_chunk_for_file:
                            chapter_title_for_db = first_chunk_for_file.chapter_title
                    
                    cur.execute("""
                        INSERT INTO document_metadata (file_path, chapter_title)
                        VALUES (%s, %s)
                        ON CONFLICT (file_path) DO UPDATE SET
                            chapter_title = EXCLUDED.chapter_title,
                            last_ingested = CURRENT_TIMESTAMP;
                    """, (file_path, chapter_title_for_db))
                conn.commit()
            conn.close()
            print("Postgres operations complete (placeholder).")
    except Exception as e:
        print(f"Error during Postgres operations: {e}")

    print("Ingestion pipeline finished.")

if __name__ == "__main__":
    # Example usage:
    # Set DOCS_PATH environment variable or pass it directly
    # For this to work, ensure Qdrant, Postgres settings are in .env
    # and OPENAI_API_KEY is set.
    # The 'my-textbook-site/docs' directory should exist relative to the project root.
    
    # Assuming current working directory is the project root (humanoid_robotics_book)
    # and the script is called from rag-service/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    docs_path = os.path.join(project_root, 'my-textbook-site', 'docs')
    
    if not os.path.exists(docs_path):
        print(f"Documentation path not found: {docs_path}")
        print("Please ensure 'my-textbook-site/docs' exists relative to project root.")
    else:
        ingestion_pipeline(docs_path)

