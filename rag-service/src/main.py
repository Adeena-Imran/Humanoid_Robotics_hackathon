from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Import services and configuration
from .config import settings
from .llm.client import LLMClient
from .llm.prompts import REFUSAL_RESPONSE, EMBEDDED_QUESTION_PROMPT, format_explanation_prompt
from .ingestion.schema import ContentChunk, ChapterSummary # For request/response schemas
from .retrieval.semantic_search import semantic_search

# --- Service Instances ---
# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot Service",
    description="API for the Retrieval-Augmented Generation (RAG) Chatbot service.",
    version="1.0.0",
)

# Pydantic models for API requests and responses (as per contracts/rag_api.yaml)
class RagChatRequest(BaseModel):
    query_type: str # explanation, chapter_summary, book_summary
    text: Optional[str] = None
    selected_text: Optional[str] = None
    chapter_id: Optional[str] = None # Using chapter_id from data model

class SourceReference(BaseModel):
    source_file: str
    chapter_title: str
    section_title: Optional[str] = None

class RagChatResponse(BaseModel):
    response: str
    sources: List[SourceReference] = []

llm_client_instance = LLMClient()

# --- T023: RefusalService ---
class RefusalService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        # A very simplified check for demonstration. A real system would use embeddings
        # to compare query to overall book content embeddings, or a dedicated classification model.
        self.out_of_scope_keywords = ["quantum computing", "space travel", "ancient history"]

    def is_query_out_of_scope(self, query: str) -> bool:
        """
        Checks if the query is likely outside the book's content.
        Simplified implementation for now; could be expanded with embedding similarity.
        """
        for keyword in self.out_of_scope_keywords:
            if keyword in query.lower():
                return True
        # More robust check: use LLM to classify if query is within book's domain
        # prompt = f"Is the following query related to 'Humanoid Robotics, AI Integration, Mechatronics, and Control'? Answer only 'yes' or 'no'. Query: '{query}'"
        # response = self.llm_client.generate_text(prompt, max_tokens=10, temperature=0.0)
        # return "no" in response.lower()
        return False # For now, assume it's in scope unless explicit keywords.

# Initialize refusal service
refusal_service_instance = RefusalService(llm_client_instance)

# --- T027: ExplanationService ---
class ExplanationService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def get_topic_explanation(self, query: str) -> RagChatResponse:
        """
        Orchestrates semantic search, gathers context, and prepares LLM prompts
        for topic-based explanations.
        """
        # 1. Perform semantic search to retrieve relevant chunks
        relevant_chunks = await semantic_search(query)

        if not relevant_chunks:
            return RagChatResponse(response=REFUSAL_RESPONSE, sources=[])

        # 2. Gather context from relevant chunks
        context_parts = [chunk.content for chunk in relevant_chunks]
        context = "\n---\n".join(context_parts)

        # 3. Prepare LLM prompt
        prompt = format_explanation_prompt(context=context, query=query)

        # 4. Generate explanation using LLM
        explanation_text = self.llm_client.generate_text(prompt)

        # 5. Prepare sources
        sources = [
            SourceReference(
                source_file=chunk.source_file,
                chapter_title=chunk.chapter_title,
                section_title=chunk.section_title
            )
            for chunk in relevant_chunks
        ]
        return RagChatResponse(response=explanation_text, sources=sources)

# Initialize explanation service
explanation_service_instance = ExplanationService(llm_client_instance)

@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot Service is running!"}

# --- T024, T025, T028: Update POST /chat endpoint ---
@app.post("/chat", response_model=RagChatResponse)
async def chat(request: RagChatRequest):
    # T024, T025: Integrate refusal_service and return refusal message
    if refusal_service_instance.is_query_out_of_scope(request.text or ""):
        return RagChatResponse(response=REFUSAL_RESPONSE, sources=[])

    if request.query_type == "explanation":
        # T028: Handle query_type: 'explanation' for topic explanations
        if not request.text:
            raise HTTPException(status_code=400, detail="'text' is required for 'explanation' query_type.")
        
        return await explanation_service_instance.get_topic_explanation(request.text)
    
    # Placeholder for other query types
    raise HTTPException(status_code=501, detail=f"Query type '{request.query_type}' not yet implemented.")