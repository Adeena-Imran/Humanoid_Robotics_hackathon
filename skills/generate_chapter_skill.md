# claude-code/skills/generate_chapter_skill.py

"""
## GenerateChapterSkill
**Description:** Generates a comprehensive Docusaurus Markdown chapter for the Physical AI & Humanoid Robotics textbook based on a given topic, including a title, introduction, learning objectives, main content, examples, a summary, and five multiple-choice questions with answers.
**Inputs:**
- `topic`: The specific subject for the chapter (e.g., "Kinematics of Robotic Arms").
**Outputs:**
- A single Docusaurus Markdown string representing the complete chapter.
**Logic Steps:**
1. Use the `BookWriterAgent` to generate the chapter title and an introductory section based on the `topic`.
2. Use the `BookWriterAgent` to generate a set of learning objectives relevant to the `topic`.
3. Use the `BookWriterAgent` to generate the main content of the chapter, including explanations, concepts, and detailed descriptions.
4. Use the `BookWriterAgent` to generate relevant examples to illustrate the concepts discussed in the main content.
5. Use the `BookWriterAgent` to generate a concise summary of the entire chapter.
6. Use the `BookWriterAgent` to generate five multiple-choice questions related to the chapter content, along with their correct answers.
7. Assemble all generated components into a single Docusaurus Markdown formatted chapter.
**Rules:**
- The generated content must be coherent, accurate, and aligned with the specified `topic`.
- All sections (title, intro, learning objectives, main content, examples, summary, MCQs) must be present in the final Markdown output.
- Multiple-choice questions must include clear answers.
- The entire output must be in valid Docusaurus Markdown format.
"""

from claude_code.agents.book_writer_agent import BookWriterAgent

class GenerateChapterSkill:
    def __init__(self):
        self.description = "Generates a comprehensive Docusaurus Markdown chapter for the Physical AI & Humanoid Robotics textbook based on a given topic, including a title, introduction, learning objectives, main content, examples, a summary, and five multiple-choice questions with answers."
        self.inputs = ["topic"]
        self.outputs = ["A single Docusaurus Markdown string representing the complete chapter."]
        self.logic_steps = [
            "Use the `BookWriterAgent` to generate the chapter title and an introductory section based on the `topic`.",
            "Use the `BookWriterAgent` to generate a set of learning objectives relevant to the `topic`.",
            "Use the `BookWriterAgent` to generate the main content of the chapter, including explanations, concepts, and detailed descriptions.",
            "Use the `BookWriterAgent` to generate relevant examples to illustrate the concepts discussed in the main content.",
            "Use the `BookWriterAgent` to generate a concise summary of the entire chapter.",
            "Use the `BookWriterAgent` to generate five multiple-choice questions related to the chapter content, along with their correct answers.",
            "Assemble all generated components into a single Docusaurus Markdown formatted chapter."
        ]
        self.rules = [
            "The generated content must be coherent, accurate, and aligned with the specified `topic`.",
            "All sections (title, intro, learning objectives, main content, examples, summary, MCQs) must be present in the final Markdown output.",
            "Multiple-choice questions must include clear answers.",
            "The entire output must be in valid Docusaurus Markdown format."
        ]
        self.book_writer_agent = BookWriterAgent()

    def execute(self, topic):
        # Placeholder for actual skill execution logic
        # This would call methods on self.book_writer_agent
        chapter_title_intro = self.book_writer_agent.generate_chapter(topic) # This is an oversimplification
        # ... more calls and assembly
        return f"# {topic} Chapter\n\n{chapter_title_intro}\n..."
