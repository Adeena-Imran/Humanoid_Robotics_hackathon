<!--
Sync Impact Report
Version change:  → 1.0.0
List of modified principles: (newly added)
Added sections:
- Agent Coordination Rules
- Output Standards
- MCP Integration Rule
- High-Level Project Purpose
Removed sections: (none)
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .gemini/commands/sp.adr.toml ⚠ pending
- .gemini/commands/sp.analyze.toml ⚠ pending
- .gemini/commands/sp.checklist.toml ⚠ pending
- .gemini/commands/sp.clarify.toml ⚠ pending
- .gemini/commands/sp.constitution.toml ⚠ pending
- .gemini/commands/sp.git.commit_pr.toml ⚠ pending
- .gemini/commands/sp.implement.toml ⚠ pending
- .gemini/commands/sp.phr.toml ⚠ pending
- .gemini/commands/sp.plan.toml ⚠ pending
- .gemini/commands/sp.specify.toml ⚠ pending
- .gemini/commands/sp.tasks.toml ⚠ pending
Follow-up TODOs: (none)
-->
# Specify+ Constitutional Framework Constitution

## Core Principles

### I. Accurate, Structured, and High-Quality Educational Content
All agents must cooperate to produce accurate, structured, and high-quality educational content.

### II. Docusaurus Optimization
Outputs must be optimized for Docusaurus documentation (MDX format).

### III. Modularity, Scalability, and Reusability
The system must be modular, scalable, and reusable across multiple chapters/modules.

### IV. Clarity, Correctness, and Explainability
All agents must follow strict clarity, correctness, and explainability rules.

### V. Safety
No harmful, unethical, or illegal content.

## Agent Coordination Rules

- book_writer_agent is the primary content generator.
- personalization_agent adapts tone, difficulty, and audience level.
- rag_content_agent retrieves contextual knowledge and supplies supporting material.

book_writer_agent must always:
- use retrieved RAG content when available.
- integrate personalization adjustments before finalizing the output.
- generate clean, well-structured MDX.

## Output Standards

All modules must:
- follow the exact structural outline provided by the user.
- use Docusaurus-friendly Markdown (MDX).
- include headings, subheadings, bullet points, and examples.
- include optional ASCII diagrams when helpful.
- be technically accurate and beginner-friendly.
- avoid fluff, repetition, and unnecessary explanations.

## MCP Integration Rule

Because this project uses Context7 MCP for documentation handling:
- All module outputs must be ready for `/docs/module-X.mdx`.
- Content must compile without errors in MDX format.
- Code blocks must be fenced with triple backticks.
- No browser-only HTML allowed unless needed.

## High-Level Project Purpose

This constitution governs the creation of a full textbook on:
**Humanoid Robotics, AI Integration, Mechatronics, and Control.**

The goal:
Produce a complete, multi-module educational resource suitable for students and engineers.

## Governance

This constitution supersedes all other practices; Amendments require documentation, approval, migration plan. All PRs/reviews must verify compliance; Complexity must be justified.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06