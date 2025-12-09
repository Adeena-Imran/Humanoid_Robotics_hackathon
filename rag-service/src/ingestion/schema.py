from pydantic import BaseModel
from typing import List, Optional

class ContentChunk(BaseModel):
    """
    Pydantic model for a content chunk, including its text, metadata, and embedding.
    """
    chunk_id: str
    source_file: str
    chapter_title: str
    section_title: Optional[str] = None
    content: str
    embedding: List[float]

class ChapterSummary(BaseModel):
    """
    Pydantic model for a pre-computed chapter summary.
    """
    chapter_title: str
    summary_text: str

if __name__ == "__main__":
    # Example usage for ContentChunk
    chunk_data = {
        "chunk_id": "intro-ch1-sec1-p1",
        "source_file": "intro.mdx",
        "chapter_title": "Introduction to Robotics",
        "section_title": "What is a Robot?",
        "content": "A robot is an autonomous machine...",
        "embedding": [0.1, 0.2, 0.3, 0.4]
    }
    chunk = ContentChunk(**chunk_data)
    print("ContentChunk example:", chunk.model_dump_json(indent=2))

    # Example usage for ChapterSummary
    summary_data = {
        "chapter_title": "Introduction to Robotics",
        "summary_text": "This chapter introduces the basics of robotics..."
    }
    summary = ChapterSummary(**summary_data)
    print("\nChapterSummary example:", summary.model_dump_json(indent=2))

