from typing import Optional, List
from pydantic import BaseModel

class RagChatRequest(BaseModel):
    query_type: str # explanation, chapter_summary, book_summary, subagent
    text: Optional[str] = None
    selected_text: Optional[str] = None
    chapter_id: Optional[str] = None # Using chapter_id from data model
    session_id: str # For context management with subagents

class SourceReference(BaseModel):
    source_file: str
    chapter_title: str
    section_title: Optional[str] = None

class RagChatResponse(BaseModel):
    response: str
    sources: List[SourceReference] = []
    citations: List[str] = [] # New field for direct citations from generated answer
