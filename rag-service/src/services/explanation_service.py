from typing import List
from ..llm.client import LLMClient
from ..llm.prompts import format_explanation_prompt, REFUSAL_RESPONSE
from ..retrieval.semantic_search import semantic_search
from ..main import RagChatResponse, SourceReference # Import schema from main for consistency

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

if __name__ == "__main__":
    # Example usage (requires LLMClient, Qdrant, config.py settings, and content ingested)
    # from ..llm.client import LLMClient
    # from ..config import settings
    # if not settings.OPENAI_API_KEY or not settings.QDRANT_URL:
    #     print("OPENAI_API_KEY and QDRANT_URL must be set to run this example.")
    # else:
    #     async def test_explanation_service():
    #         llm_client = LLMClient()
    #         explanation_service = ExplanationService(llm_client)
    #         print("Testing ExplanationService:")
    #         query = "What is forward kinematics?"
    #         response = await explanation_service.get_topic_explanation(query)
    #         print(f"\nExplanation: {response.response}")
    #         print(f"Sources: {response.sources}")

    #     import asyncio
    #     asyncio.run(test_explanation_service())
    pass
