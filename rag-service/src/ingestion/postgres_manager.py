import psycopg2
from psycopg2 import errors
from typing import Optional, List
from datetime import datetime
from ..db.postgres import get_postgres_connection
from ..ingestion.schema import ChapterSummary

class PostgresManager:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = get_postgres_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create_metadata_tables(self):
        """
        Creates necessary tables in Neon Postgres for document metadata and chapter summaries.
        """
        with self.conn.cursor() as cur:
            # Table for tracking ingested document metadata
            cur.execute("""
                CREATE TABLE IF NOT EXISTS document_metadata (
                    id SERIAL PRIMARY KEY,
                    file_path TEXT UNIQUE NOT NULL,
                    chapter_title TEXT,
                    last_ingested TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Table for pre-computed chapter summaries
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chapter_summaries (
                    chapter_id TEXT PRIMARY KEY NOT NULL,
                    chapter_title TEXT UNIQUE NOT NULL,
                    summary_text TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
        print("Postgres metadata tables created or already exist.")

    def upsert_document_metadata(self, file_path: str, chapter_title: Optional[str] = None):
        """
        Upserts (inserts or updates) metadata for an ingested document.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO document_metadata (file_path, chapter_title)
                VALUES (%s, %s)
                ON CONFLICT (file_path) DO UPDATE SET
                    chapter_title = EXCLUDED.chapter_title,
                    last_ingested = CURRENT_TIMESTAMP;
            """, (file_path, chapter_title))
            self.conn.commit()
        print(f"Upserted metadata for document: {file_path}")

    def upsert_chapter_summary(self, summary: ChapterSummary):
        """
        Upserts (inserts or updates) a pre-computed chapter summary.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chapter_summaries (chapter_id, chapter_title, summary_text)
                VALUES (%s, %s, %s)
                ON CONFLICT (chapter_id) DO UPDATE SET
                    chapter_title = EXCLUDED.chapter_title,
                    summary_text = EXCLUDED.summary_text,
                    last_updated = CURRENT_TIMESTAMP;
            """, (summary.chapter_title.lower().replace(" ", "-"), summary.chapter_title, summary.summary_text)) # Using slug for chapter_id
            self.conn.commit()
        print(f"Upserted summary for chapter: {summary.chapter_title}")

    def get_chapter_summary(self, chapter_title: str) -> Optional[ChapterSummary]:
        """
        Retrieves a chapter summary by its title.
        """
        chapter_id = chapter_title.lower().replace(" ", "-")
        with self.conn.cursor() as cur:
            cur.execute("SELECT chapter_title, summary_text FROM chapter_summaries WHERE chapter_id = %s;", (chapter_id,))
            record = cur.fetchone()
            if record:
                return ChapterSummary(chapter_title=record[0], summary_text=record[1])
        return None

if __name__ == "__main__":
    # Example usage:
    try:
        with PostgresManager() as manager:
            manager.create_metadata_tables()
            
            # Example document metadata upsert
            manager.upsert_document_metadata("test_doc.mdx", "Test Chapter One")
            
            # Example chapter summary upsert
            sample_summary = ChapterSummary(
                chapter_title="Test Chapter One",
                summary_text="This is a test summary for Test Chapter One."
            )
            manager.upsert_chapter_summary(sample_summary)

            # Example retrieve chapter summary
            retrieved_summary = manager.get_chapter_summary("Test Chapter One")
            if retrieved_summary:
                print(f"\nRetrieved Summary: {retrieved_summary.chapter_title} - {retrieved_summary.summary_text}")
            
    except OperationalError as e:
        print(f"Database operation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
