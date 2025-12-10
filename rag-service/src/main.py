from typing import Optional, List, Dict
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status

# Import services and configuration
from .config.settings import settings
from .llm.client import LLMClient
from .llm.prompts import REFUSAL_RESPONSE, EMBEDDED_QUESTION_PROMPT, format_explanation_prompt
from .ingestion.schema import ContentChunk, ChapterSummary # For request/response schemas
from .retrieval.semantic_search import semantic_search
from .services.subagent_service import SubagentService
from .services.skill_service import SkillService
from .services.context_service import ContextService
from .services.grounding_service import GroundingService, RetrievedChunk # Import RetrievedChunk for semantic_search
from .services.answer_generation_service import AnswerGenerationService, GeneratedAnswer
from .services.hallucination_guard import HallucinationGuardService
from .utils.request_validator import RequestValidator
from .middleware.rate_limiter import RateLimiterMiddleware
from .utils.api_errors import BaseAPIException, APIError, ErrorDetail # Import custom exceptions and error models
from .utils.healthcheck import HealthCheckService # Import HealthCheckService
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Add this line
from pydantic import BaseModel

# --- Service Instances ---
# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming Docusaurus dev server runs on port 3000
    # You might need to add other origins if your frontend is hosted elsewhere
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply Rate Limiting Middleware
app.add_middleware(RateLimiterMiddleware)

# --- Exception Handler for custom API exceptions ---
@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_api_error().model_dump()
    )

# --- Startup Event Handler for Health Checks ---
@app.on_event("startup")
async def startup_event():
    health_checker = HealthCheckService()
    await health_checker.run_startup_checks()

from .schemas import RagChatRequest, SourceReference, RagChatResponse

llm_client_instance = LLMClient()

# Initialize subagent, skill, and context services
subagent_service_instance = SubagentService()
skill_service_instance = SkillService()
context_service_instance = ContextService()
grounding_service_instance = GroundingService()
answer_generation_service_instance = AnswerGenerationService(llm_client_instance)
hallucination_guard_service_instance = HallucinationGuardService(llm_client_instance)

# --- Constants ---
# Moved to settings.CONFIDENCE_THRESHOLD # Minimum confidence score for an answer to be returned

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
        for keyword in query.lower():
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
    # T048: Run RequestValidator before any processing
    # RequestValidator.validate_chat_payload(request) # Commented out for debugging

    # T024, T025: Integrate refusal_service and return refusal message
    if refusal_service_instance.is_query_out_of_scope(request.text or ""):
        return RagChatResponse(response=REFUSAL_RESPONSE, sources=[])

    session_id = request.session_id # session_id is guaranteed to be present by validator

    if request.query_type == "explanation":
        # T028: Handle query_type: 'explanation' for topic explanations
        # 'text' is guaranteed to be present by validator
        
        # --- T044: Enforce: retrieve -> ground -> generate -> validate ---

        # 1. Retrieve: Perform semantic search to retrieve relevant chunks (using existing semantic_search)
        relevant_chunks_from_db = await semantic_search(request.text)

        if not relevant_chunks_from_db:
            return RagChatResponse(response=REFUSAL_RESPONSE, sources=[], citations=[])

        # Convert database chunks to RetrievedChunk model for GroundingService
        # semantic_search returns ContentChunk, so we need to map to RetrievedChunk
        retrieved_chunks_for_grounding = [
            RetrievedChunk(
                content=chunk.content,
                doc_id=chunk.source_file, # Assuming source_file maps to doc_id
                chunk_id=f"{chunk.chapter_title}_{chunk.section_title}", # Create a unique chunk_id
                score=1.0, # Placeholder score, as semantic_search doesn't return it currently
                chapter_title=chunk.chapter_title,
                section_title=chunk.section_title
            ) for chunk in relevant_chunks_from_db
        ]

        # 2. Ground: Prepare grounded evidence blocks
        grounded_evidence = grounding_service_instance.ground_chunks(retrieved_chunks_for_grounding)
        
        if not grounded_evidence:
            return RagChatResponse(response=REFUSAL_RESPONSE, sources=[], citations=[]) # No grounded evidence after processing

        # 3. Generate: Generate answer using grounded evidence
        try:
            generated_answer = await answer_generation_service_instance.generate_answer(
                query=request.text,
                grounded_evidence=grounded_evidence
            )
        except ValueError as e:
            raise HTTPException(status_code=500, detail=f"Answer generation failed: {e}")

        # 4. Validate: Detect unsupported claims and get confidence score
        confidence = await hallucination_guard_service_instance.check_answer_grounding(
            generated_answer=generated_answer,
            grounded_evidence=grounded_evidence
        )

        # 5. If confidence < threshold, return refusal / fallback message
        if confidence < settings.CONFIDENCE_THRESHOLD:
            return RagChatResponse(
                response="I cannot confidently answer your question based on the available information. Please try rephrasing or asking a different question.",
                sources=[],
                citations=[]
            )
        
        # 6. Include citations in final response payload
        # Prepare sources from the original relevant_chunks_from_db to show what was considered.
        sources = [
            SourceReference(
                source_file=chunk.source_file,
                chapter_title=chunk.chapter_title,
                section_title=chunk.section_title
            )
            for chunk in relevant_chunks_from_db
        ]

        return RagChatResponse(
            response=generated_answer.answer,
            sources=sources,
            citations=generated_answer.citations
        )

    elif request.query_type == "subagent":
        # 'text' is guaranteed to be present by validator
        
        # Simple subagent selection logic: assume text contains "subagent_name: skill_name" for now
        # A more sophisticated approach would use an LLM to determine intent and subagent.
        try:
            subagent_name, skill_to_execute = request.text.split(":", 1)
            subagent_name = subagent_name.strip()
            skill_to_execute = skill_to_execute.strip()
        except ValueError: # This should ideally be caught by the validator already for subagent type
            raise HTTPException(status_code=400, detail="Invalid format for 'subagent' query_type. Expected 'subagent_name: skill_name'.")

        # 1. Retrieve subagent (T039 requirement)
        subagent = await subagent_service_instance.get_subagent(subagent_name)
        if not subagent:
            raise HTTPException(status_code=404, detail=f"Subagent '{subagent_name}' not found.")
        
        # 2. Retrieve context for the subagent (T039 requirement)
        current_context = await context_service_instance.get_context(subagent_name, session_id)
        if not current_context:
            current_context = {} # Initialize if no context exists

        # For this example, let's assume a simple skill chain for any subagent
        # In a real scenario, this would be defined per subagent or dynamically determined.
        # We also need a way to map skill_to_execute to an actual callable.
        # For now, we'll use a placeholder skill list for the skill_service.
        skills_to_chain = [
            {"name": "pre_process_query"},
            {"name": skill_to_execute}, # The specific skill requested
            {"name": "post_process_response"}
        ]

        # Prepare input for the skill chain
        skill_input = {
            "query": request.text,
            "session_id": session_id,
            "context": current_context,
            "chapter_id": request.chapter_id,
            "selected_text": request.selected_text,
            # Merging Qdrant results would happen here or within the skill itself if it needs it.
            # For T038 context merge, this is where we'd pass combined context.
        }

        # 3. Execute skill chain (T039 requirement)
        try:
            skill_chain_result = await skill_service_instance.execute_skill_chain(
                subagent_name=subagent_name,
                skills=skills_to_chain,
                input_data=skill_input
            )
            final_response = skill_chain_result.get("final_output", "Subagent processed your request.")
            
            # Assuming the skill chain might update context, save it back
            updated_context = skill_chain_result.get("execution_log", {}).get("updated_context", current_context)
            await context_service_instance.save_context(subagent_name, session_id, updated_context)

            return RagChatResponse(response=final_response, sources=[], citations=[])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Subagent skill chain failed: {e}")
    
    raise HTTPException(status_code=501, detail=f"Query type '{request.query_type}' not yet implemented.")