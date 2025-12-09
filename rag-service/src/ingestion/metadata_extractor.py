import hashlib
from typing import Dict, Any, List
from ..ingestion.schema import ContentChunk

def generate_chunk_id(content: str, metadata: Dict[str, Any]) -> str:
    """
    Generates a unique ID for a chunk based on its content and key metadata.
    """
    # Create a hash from content and significant metadata to ensure uniqueness
    # and consistency if content/metadata doesn't change.
    unique_string = f"{content}-{metadata.get('source_file')}-{metadata.get('chapter_title')}-{metadata.get('section_title')}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

def extract_and_format_metadata(raw_chunk_data: Dict[str, Any], embedding: List[float]) -> ContentChunk:
    """
    Takes raw chunk data (from chunker) and an embedding,
    then formats it into a ContentChunk Pydantic model.
    """
    chunk_id = generate_chunk_id(raw_chunk_data['content'], raw_chunk_data)
    
    return ContentChunk(
        chunk_id=chunk_id,
        source_file=raw_chunk_data['source_file'],
        chapter_title=raw_chunk_data['chapter_title'],
        section_title=raw_chunk_data.get('section_title'), # Optional
        content=raw_chunk_data['content'],
        embedding=embedding # Embedding is passed in after generation
    )

if __name__ == "__main__":
    # Example usage:
    raw_data = {
        "content": "This is a sample paragraph about robots.",
        "source_file": "intro.mdx",
        "chapter_title": "Introduction",
        "section_title": "Overview"
    }
    sample_embedding = [0.1, 0.2, 0.3, 0.4, 0.5] # Dummy embedding

    formatted_chunk = extract_and_format_metadata(raw_data, sample_embedding)
    print(formatted_chunk.model_dump_json(indent=2))