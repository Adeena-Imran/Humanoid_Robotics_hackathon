from typing import Dict, Any, List
from openai import OpenAI
from ..config.settings import settings

class LLMClient:
    def __init__(self):
        if not settings.LLM_API_KEY:
            raise ValueError("LLM_API_KEY is not set in configuration.")
        self.client = OpenAI(api_key=settings.LLM_API_KEY)
        self.default_model = settings.LLM_MODEL # Use model from settings
        self.default_temperature = settings.LLM_TEMPERATURE # Use temperature from settings

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generates text using the OpenAI Chat Completion API.
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = await self.client.chat.completions.create(
                model=kwargs.get("model", self.default_model),
                messages=messages,
                temperature=kwargs.get("temperature", self.default_temperature),
                max_tokens=kwargs.get("max_tokens", 500),
                **kwargs.get("openai_extra_params", {})
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text with LLM: {e}")
            raise

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generates embeddings for the given text using the OpenAI Embedding API.
        """
        try:
            response = await self.client.embeddings.create(
                input=[text],
                model="text-embedding-ada-002" # Or another suitable embedding model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding with LLM: {e}")
            raise

if __name__ == "__main__":
    # Example usage:
    async def run_examples():
        # Temporarily set API key for example if not set in .env
        import os
        if "LLM_API_KEY" not in os.environ:
            os.environ["LLM_API_KEY"] = "sk-mock-key" # Placeholder for local testing

        try:
            llm_client = LLMClient()
            test_prompt = "What is the capital of France?"
            print(f"Generating text for: '{test_prompt}'")
            response_text = await llm_client.generate_text(test_prompt)
            print(f"LLM Response: {response_text}")

            # Example with specific model and temperature
            print("\nGenerating with specific parameters:")
            response_text_tuned = await llm_client.generate_text(
                "Write a very short, cheerful haiku about a cat.",
                model="gpt-3.5-turbo",
                temperature=0.9,
                max_tokens=50
            )
            print(f"LLM Response (tuned): {response_text_tuned}")

            # Test embedding
            print("\nGenerating embedding:")
            embedding = await llm_client.get_embedding("Hello, world!")
            print(f"Embedding length: {len(embedding)}")
            print(f"First 5 embedding values: {embedding[:5]}")

        except ValueError as e:
            print(f"Configuration Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Ensure LLM_API_KEY is set and valid.")

    import asyncio
    asyncio.run(run_examples())
