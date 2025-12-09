from typing import Dict, Any
from openai import OpenAI
from ..config import settings

class LLMClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in configuration.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.default_model = "gpt-3.5-turbo" # Or "gpt-4", based on cost/performance needs

    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generates text using the OpenAI Chat Completion API.
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.default_model),
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 500),
                **kwargs.get("openai_extra_params", {})
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text with LLM: {e}")
            raise

if __name__ == "__main__":
    # Example usage:
    try:
        llm_client = LLMClient()
        test_prompt = "What is the capital of France?"
        print(f"Generating text for: '{test_prompt}'")
        response_text = llm_client.generate_text(test_prompt)
        print(f"LLM Response: {response_text}")

        # Example with specific model and temperature
        print("\nGenerating with specific parameters:")
        response_text_tuned = llm_client.generate_text(
            "Write a very short, cheerful haiku about a cat.",
            model="gpt-3.5-turbo",
            temperature=0.9,
            max_tokens=50
        )
        print(f"LLM Response (tuned): {response_text_tuned}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Ensure OPENAI_API_KEY is set and valid.")
