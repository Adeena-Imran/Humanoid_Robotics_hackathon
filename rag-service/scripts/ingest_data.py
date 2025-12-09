import os
import argparse
from datetime import datetime
from ..src.ingestion.pipeline import ingestion_pipeline
from ..src.ingestion.postgres_manager import PostgresManager
from ..src.ingestion.qdrant_manager import create_qdrant_collection, QDRANT_COLLECTION_NAME
from ..src.config import settings # Ensure settings are loaded

def main():
    parser = argparse.ArgumentParser(description="Run the RAG data ingestion pipeline.")
    parser.add_argument(
        "--docs-path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), '../../my-textbook-site/docs'),
        help="Path to the directory containing Markdown/MDX documentation files."
    )
    parser.add_argument(
        "--create-tables",
        action="store_true",
        help="Create Qdrant collection and Postgres tables before ingestion."
    )
    args = parser.parse_args()

    # Ensure environment variables are loaded (already done by config.py import)
    # validate essential settings
    if not settings.QDRANT_URL or not settings.POSTGRES_URL:
        print("Error: Essential environment variables (QDRANT_URL, POSTGRES_URL) are not set.")
        print("Please configure your .env file in rag-service/ directory.")
        return

    if args.create_tables:
        print("Creating Qdrant collection and Postgres metadata tables...")
        try:
            create_qdrant_collection(collection_name=QDRANT_COLLECTION_NAME)
            with PostgresManager() as pg_manager:
                pg_manager.create_metadata_tables()
            print("Tables and collections created successfully.")
        except Exception as e:
            print(f"Error creating tables/collections: {e}")
            return
    
    print(f"Starting data ingestion at {datetime.now()} for docs_path: {args.docs_path}")
    ingestion_pipeline(args.docs_path)
    print(f"Data ingestion finished at {datetime.now()}")

if __name__ == "__main__":
    main()
