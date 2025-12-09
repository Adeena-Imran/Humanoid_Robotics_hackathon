from typing import List

# Base system prompt as defined in the spec
BASE_SYSTEM_PROMPT = """
You are a helpful assistant for the book "Humanoid Robotics: From Theory to Practice".
Your role is to answer questions and provide explanations based ONLY on the provided context from the book.
Do not use any external knowledge. If the answer cannot be found in the provided context, state that clearly.
Be concise and directly address the user's question.
"""

# Prompt for general explanations (topic-based or selected-text)
EXPLANATION_PROMPT_TEMPLATE = BASE_SYSTEM_PROMPT + """

CONTEXT FROM THE BOOK:
---
{context}
---

QUESTION:
\"{query}\" 

Based on the context provided, please explain the following:
"""

# Prompt for chapter summaries
CHAPTER_SUMMARY_PROMPT_TEMPLATE = BASE_SYSTEM_PROMPT + """

CONTEXT FROM CHAPTER \"{chapter_title}\" OF THE BOOK:
---
{context}
---

Based on the context provided, generate a concise summary of this chapter. The format of the summary should be adaptive, considering the content, and could be a bulleted list, multiple paragraphs, or a single concise paragraph.
"""

# Prompt for whole-book summaries
WHOLE_BOOK_SUMMARY_PROMPT_TEMPLATE = BASE_SYSTEM_PROMPT + """

CONTEXT - CHAPTER SUMMARIES FROM THE BOOK:
---
{chapter_summaries_context}
---

Based on the chapter summaries provided, generate a high-level summary of the entire book, highlighting its main themes and progression of topics.
"""

# Refusal prompt when content is outside book scope
REFUSAL_RESPONSE = "This topic is not covered in the book."

# Prompt to handle embedded questions in summary requests (as per spec)
EMBEDDED_QUESTION_PROMPT = """
I have provided the summary for your requested chapter. If you still wish to ask about \"{embedded_question}\", please ask it as a separate question.
"""

def format_explanation_prompt(context: str, query: str) -> str:
    return EXPLANATION_PROMPT_TEMPLATE.format(context=context, query=query)

def format_chapter_summary_prompt(chapter_title: str, context: str) -> str:
    return CHAPTER_SUMMARY_PROMPT_TEMPLATE.format(chapter_title=chapter_title, context=context)

def format_whole_book_summary_prompt(chapter_summaries: List[str]) -> str:
    chapter_summaries_context = "\n---\n".join(chapter_summaries)
    return WHOLE_BOOK_SUMMARY_PROMPT_TEMPLATE.format(chapter_summaries_context=chapter_summaries_context)

if __name__ == "__main__":
    # Example usage:
    print("---"Explanation Prompt"---")
    print(format_explanation_prompt("The quick brown fox jumps over the lazy dog.", "What is a fox?"))
    
    print("\n---"Chapter Summary Prompt"---")
    print(format_chapter_summary_prompt("Animals", "Foxes are mammals. Dogs are also mammals."))
    
    print("\n---"Whole Book Summary Prompt"---")
    print(format_whole_book_summary_prompt(["Chapter 1: About Foxes.", "Chapter 2: About Dogs."]))

    print("\n---"Refusal Response"---")
    print(REFUSAL_RESPONSE)

    print("\n---"Embedded Question Prompt"---")
    print(EMBEDDED_QUESTION_PROMPT.format(embedded_question="PID controller"))