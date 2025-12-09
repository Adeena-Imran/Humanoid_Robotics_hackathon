from ..llm.client import LLMClient
from ..llm.prompts import REFUSAL_RESPONSE
from typing import List

class RefusalService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        # A very simplified check for demonstration. A real system would use embeddings
        # to compare query to overall book content embeddings, or training a classifier.
        # This list should be managed more robustly, perhaps from config or a DB.
        self.out_of_scope_keywords = [
            "quantum computing", "space travel", "ancient history",
            "cooking recipes", "latest fashion trends", "celebrity gossip"
        ]
        
    async def is_query_out_of_scope(self, query: str) -> bool:
        """
        Checks if the query is likely outside the book's content.
        This is a simplified implementation.
        More robust checks could involve:
        - Comparing query embedding to average embedding of all book content.
        - A dedicated LLM call with a finely tuned prompt to classify the query's domain.
        - Pre-defined list of allowed/disallowed topics.
        """
        lower_query = query.lower()
        for keyword in self.out_of_scope_keywords:
            if keyword in lower_query:
                return True
        
        # Further LLM-based check (optional, more compute intensive)
        # prompt = f"""
        # Given the book is about "Humanoid Robotics, AI Integration, Mechatronics, and Control",
        # is the following query relevant to the book's topics?
        # Answer only 'yes' or 'no'.
        # Query: '{query}'
        # """
        # response = await self.llm_client.generate_text(prompt, max_tokens=10, temperature=0.0)
        # return "no" in response.lower().strip()
        
        return False # For now, assume it's in scope unless explicit keywords are found.

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY and a running LLMClient setup)
    # from ..config import settings
    # if not settings.OPENAI_API_KEY:
    #     print("OPENAI_API_KEY not set. Cannot run LLM-based refusal check example.")
    # else:
    #     llm_client = LLMClient()
    #     refusal_service = RefusalService(llm_client)

    #     async def test_refusal_service():
    #         print("Testing RefusalService:")
    #         print(f"Query 'What is quantum computing?': {await refusal_service.is_query_out_of_scope('What is quantum computing?')}")
    #         print(f"Query 'Explain inverse kinematics': {await refusal_service.is_query_out_of_scope('Explain inverse kinematics')}")
        
    #     import asyncio
    #     asyncio.run(test_refusal_service())
    pass