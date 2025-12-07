# Quickstart

This document explains how to generate the content for the humanoid robotics textbook.

## Prerequisites

-   An environment with the Gemini CLI and the necessary agents (`rag_content_agent`, `personalization_agent`, `book_writer_agent`) configured.

## Generation Pipeline

The content generation follows a multi-agent pipeline:

1.  **RAG Content Agent (`rag_content_agent`)**: Gathers contextual knowledge and relevant information to support the content.
2.  **Personalization Agent (`personalization_agent`)**: Adjusts the tone, difficulty, and audience level of the content.
3.  **Book Writer Agent (`book_writer_agent`)**: Generates the final Docusaurus-compatible MDX module.

## Running the Pipeline

To generate a module, you will typically use a high-level command that orchestrates these agents. For example:

`/generate_module "Introduction to Humanoid Robotics"`

This command would trigger the pipeline and output the final `module-1.mdx` file to the `/docs` directory.
