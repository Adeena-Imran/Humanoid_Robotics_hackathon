# claude-code/agents/book_writer_agent.py

"""
## BookWriterAgent
**Description:** Writes educational content for the Physical AI & Humanoid Robotics textbook, including chapters, learning objectives, quizzes, diagrams (text), summaries, and exercises.
**Inputs:**
- Chapter topics
- Learning objective prompts
- Quiz content requirements
- Diagram (textual representation) descriptions
- Summary prompts
- Exercise prompts
**Outputs:**
- Docusaurus Markdown formatted chapters
- Docusaurus Markdown formatted learning objectives
- Docusaurus Markdown formatted quizzes
- Docusaurus Markdown formatted diagrams (textual)
- Docusaurus Markdown formatted summaries
- Docusaurus Markdown formatted exercises
**Functions / Capabilities:**
- Content generation (chapters, objectives, quizzes, summaries, exercises)
- Text-based diagram generation
- Docusaurus Markdown formatting
**Rules:**
- Content must be technically accurate and pedagogically sound.
- All output must strictly adhere to Docusaurus Markdown formatting.
- Diagrams are generated as descriptive text, not visual images.
"""

class BookWriterAgent:
    def __init__(self):
        self.description = "Writes educational content for the Physical AI & Humanoid Robotics textbook, including chapters, learning objectives, quizzes, diagrams (text), summaries, and exercises."
        self.inputs = [
            "Chapter topics",
            "Learning objective prompts",
            "Quiz content requirements",
            "Diagram (textual representation) descriptions",
            "Summary prompts",
            "Exercise prompts"
        ]
        self.outputs = [
            "Docusaurus Markdown formatted chapters",
            "Docusaurus Markdown formatted learning objectives",
            "Docusaurus Markdown formatted quizzes",
            "Docusaurus Markdown formatted diagrams (textual)",
            "Docusaurus Markdown formatted summaries",
            "Docusaurus Markdown formatted exercises"
        ]
        self.functions_capabilities = [
            "Content generation (chapters, objectives, quizzes, summaries, exercises)",
            "Text-based diagram generation",
            "Docusaurus Markdown formatting"
        ]
        self.rules = [
            "Content must be technically accurate and pedagogically sound.",
            "All output must strictly adhere to Docusaurus Markdown formatting.",
            "Diagrams are generated as descriptive text, not visual images."
        ]

    def generate_chapter(self, topic):
        # Placeholder for actual chapter generation logic
        pass

    def generate_quiz(self, content):
        # Placeholder for actual quiz generation logic
        pass

    # ... other methods for generating diagrams, summaries, exercises
