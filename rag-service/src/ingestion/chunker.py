from typing import List, Dict, Any, Optional
import markdown_it
import hashlib

# Markdown parser setup
md = markdown_it.MarkdownIt()

def chunk_markdown(markdown_content: str, source_file: str) -> List[Dict[str, Any]]:
    """
    Chunks Markdown content hierarchically (chapter -> section -> paragraph).
    Extracts basic metadata (chapter_title, section_title) during chunking.
    """
    chunks = []
    current_chapter = "Introduction" # Default for content before first H1
    current_section = None
    
    # Render markdown to tokens for easier parsing of structure
    tokens = md.parse(markdown_content)
    
    current_text_buffer = []
    
    def _flush_buffer():
        nonlocal current_text_buffer
        if current_text_buffer:
            content = "\n".join(current_text_buffer).strip()
            if content:
                chunks.append({
                    "content": content,
                    "source_file": source_file,
                    "chapter_title": current_chapter,
                    "section_title": current_section,
                })
            current_text_buffer = []

    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            _flush_buffer() # Flush any buffered text before a new heading
            level = int(token.tag[1]) # e.g., 'h1' -> 1, 'h2' -> 2
            
            # Get the content of the heading (next token)
            heading_content_token = tokens[i+1]
            if heading_content_token.type == 'inline':
                heading_text = heading_content_token.content.strip()

                if level == 1: # Chapter
                    current_chapter = heading_text
                    current_section = None # Reset section for new chapter
                elif level == 2 or level == 3: # Section or Subsection
                    current_section = heading_text
                # For levels > 3, we might treat them as part of the current section
                # or ignore for primary chunking hierarchy. For now, group with section.
                
        elif token.type == 'paragraph_open':
            # Collect text until paragraph_close
            paragraph_content = []
            j = i + 1
            while j < len(tokens) and tokens[j].type != 'paragraph_close':
                if tokens[j].type == 'inline':
                    paragraph_content.append(tokens[j].content)
                j += 1
            
            _flush_buffer() # Flush any text before this new paragraph
            current_text_buffer.append(" ".join(paragraph_content).strip())
            
        elif token.type == 'inline' and tokens[i-1].type != 'heading_open':
            # This handles inline content that is not part of a paragraph (e.g., list items, blockquotes)
            # For simplicity, we'll buffer it if it's not a heading or paragraph
            # More complex logic for lists etc. might be needed for perfect fidelity
            if tokens[i-1].type not in ['paragraph_open', 'list_item_open', 'blockquote_open']:
                 current_text_buffer.append(token.content.strip())
                 
    _flush_buffer() # Flush any remaining text at the end

    return chunks

if __name__ == "__main__":
    example_md = """
# Chapter 1: Introduction

This is the introduction.

## Section 1.1: Basics

Some text about basics.

Another paragraph in basics.

### Subsection 1.1.1: Details

More detailed text here.

* Item 1
* Item 2

## Section 1.2: Advanced

Advanced concepts.
"""
    
    chunked_data = chunk_markdown(example_md, "example.md")
    for i, chunk in enumerate(chunked_data):
        print(f"--- Chunk {i+1} ---")
        print(f"Source: {chunk['source_file']}")
        print(f"Chapter: {chunk['chapter_title']}")
        print(f"Section: {chunk['section_title']}")
        print(f"Content:\n{chunk['content']}\n")
