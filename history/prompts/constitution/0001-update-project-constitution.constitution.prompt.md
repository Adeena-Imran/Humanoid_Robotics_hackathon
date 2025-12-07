---
id: 0001
title: Update Project Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: gemini-1.5-flash
feature: none
branch: 001-humanoid-robotics-modules
user: PMLS
command: /sp.constitution You are operating under the Specify+ Constitutional Framework.

## CORE PRINCIPLES
1. All agents must cooperate to produce accurate, structured, and high-quality educational content.
2. Outputs must be optimized for Docusaurus documentation (MDX format).
3. The system must be modular, scalable, and reusable across multiple chapters/modules.
4. All agents must follow strict clarity, correctness, and explainability rules.
5. Safety: No harmful, unethical, or illegal content.

## AGENT COORDINATION RULES
- book_writer_agent is the primary content generator.
- personalization_agent adapts tone, difficulty, and audience level.
- rag_content_agent retrieves contextual knowledge and supplies supporting material.

book_writer_agent must always:
- use retrieved RAG content when available.
- integrate personalization adjustments before finalizing the output.
- generate clean, well-structured MDX.

## OUTPUT STANDARDS
All modules must:
- follow the exact structural outline provided by the user.
- use Docusaurus-friendly Markdown (MDX).
- include headings, subheadings, bullet points, and examples.
- include optional ASCII diagrams when helpful.
- be technically accurate and beginner-friendly.
- avoid fluff, repetition, and unnecessary explanations.

## MCP INTEGRATION RULE
Because this project uses Context7 MCP for documentation handling:
- All module outputs must be ready for `/docs/module-X.mdx`.
- Content must compile without errors in MDX format.
- Code blocks must be fenced with triple backticks.
- No browser-only HTML allowed unless needed.

## HIGH-LEVEL PROJECT PURPOSE
This constitution governs the creation of a full textbook on:
**Humanoid Robotics, AI Integration, Mechatronics, and Control.**

The goal:
Produce a complete, multi-module educational resource suitable for students and engineers.

End of constitution.
labels: ["constitution", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:

---

## Prompt

/sp.constitution You are operating under the Specify+ Constitutional Framework.

## CORE PRINCIPLES
1. All agents must cooperate to produce accurate, structured, and high-quality educational content.
2. Outputs must be optimized for Docusaurus documentation (MDX format).
3. The system must be modular, scalable, and reusable across multiple chapters/modules.
4. All agents must follow strict clarity, correctness, and explainability rules.
5. Safety: No harmful, unethical, or illegal content.

## AGENT COORDINATION RULES
- book_writer_agent is the primary content generator.
- personalization_agent adapts tone, difficulty, and audience level.
- rag_content_agent retrieves contextual knowledge and supplies supporting material.

book_writer_agent must always:
- use retrieved RAG content when available.
- integrate personalization adjustments before finalizing the output.
- generate clean, well-structured MDX.

## OUTPUT STANDARDS
All modules must:
- follow the exact structural outline provided by the user.
- use Docusaurus-friendly Markdown (MDX).
- include headings, subheadings, bullet points, and examples.
- include optional ASCII diagrams when helpful.
- be technically accurate and beginner-friendly.
- avoid fluff, repetition, and unnecessary explanations.

## MCP INTEGRATION RULE
Because this project uses Context7 MCP for documentation handling:
- All module outputs must be ready for `/docs/module-X.mdx`.
- Content must compile without errors in MDX format.
- Code blocks must be fenced with triple backticks.
- No browser-only HTML allowed unless needed.

## HIGH-LEVEL PROJECT PURPOSE
This constitution governs the creation of a full textbook on:
**Humanoid Robotics, AI Integration, Mechatronics, and Control.**

The goal:
Produce a complete, multi-module educational resource suitable for students and engineers.

End of constitution.

## Response snapshot

Updated project constitution to v1.0.0. Manual follow-up needed for templates and command files. Suggested commit: docs: amend constitution to v1.0.0 (initial setup).

## Outcome

- ✅ Impact: Project constitution updated and aligned with user-provided principles and rules.
- 🧪 Tests: N/A
- 📁 Files: Updated `.specify/memory/constitution.md`.
- 🔁 Next prompts: The user needs to manually update the listed templates and command files to align with the new constitution.
- 🧠 Reflection: Successfully updated the project constitution based on user input, expanding the template to accommodate additional sections. Noted pending manual updates for other templates.

## Evaluation notes (flywheel)

- Failure modes observed: (empty)
- Graders run and results (PASS/FAIL): (empty)
- Prompt variant (if applicable): (empty)
- Next experiment (smallest change to try): (empty)
