# rag-service/tests/test_integration.py

import unittest
import os
import sys
import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

# Add the parent directory (rag-service) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services import neon_helpers, conversation_service

# Load environment variables from a .env file if it exists
load_dotenv()


class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the necessary clients and test data for all tests in this class.
        """
        # --- Neon DB Setup ---
        cls.neon_url = os.environ.get("NEON_DATABASE_URL")
        if not cls.neon_url:
            raise unittest.SkipTest("NEON_DATABASE_URL not set. Skipping integration tests.")

        # Initialize the database (creates tables)
        conversation_service.initialize_database()

        # --- Qdrant Setup ---
        cls.qdrant_url = os.environ.get("QDRANT_URL")
        cls.qdrant_api_key = os.environ.get("QDRANT_API_KEY")
        if not cls.qdrant_url:
            raise unittest.SkipTest("QDRANT_URL not set. Skipping integration tests.")

        cls.qdrant_client = QdrantClient(
            url=cls.qdrant_url,
            api_key=cls.qdrant_api_key,
        )

        # --- Test Data ---
        cls.test_session_id = "integration-test-session-123"
        cls.vector_size = 4  # Example vector size
        cls.collection_name = "test_conversation_embeddings"

    def setUp(self):
        """
        Create a fresh Qdrant collection before each test.
        """
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def tearDown(self):
        """
        Clean up created data after each test.
        """
        conn = None
        try:
            conn = conversation_service.get_neondb_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM conversations WHERE session_id = %s",
                (self.test_session_id,),
            )
            cursor.execute(
                "DELETE FROM conversation_metadata WHERE session_id = %s",
                (self.test_session_id,),
            )
            conn.commit()
            cursor.close()
        finally:
            if conn:
                conversation_service.close_neondb_connection(conn)

        # Delete the Qdrant collection
        self.qdrant_client.delete_collection(
            collection_name=self.collection_name
        )

    def test_conversation_storage_and_embedding_retrieval(self):
        """
        End-to-end test:
        1. Store conversation messages and metadata in Neon.
        2. Verify storage and retrieval from Neon.
        3. Create and store embeddings in Qdrant.
        4. Retrieve embeddings from Qdrant and verify results.
        """

        # --- 1. Store in Neon ---
        messages = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
        ]

        for msg in messages:
            neon_helpers.save_message(
                self.test_session_id,
                msg["role"],
                msg["content"],
            )

        metadata = {"topic": "geography", "user_id": "test-user"}
        neon_helpers.update_metadata(
            self.test_session_id,
            metadata,
        )

        # --- 2. Verify Neon Storage ---
        retrieved_conversation = neon_helpers.get_conversation(
            self.test_session_id
        )
        self.assertEqual(len(retrieved_conversation), len(messages))
        self.assertEqual(
            retrieved_conversation[0][1],
            messages[0]["content"],
        )

        retrieved_metadata = neon_helpers.get_metadata(
            self.test_session_id
        )
        self.assertEqual(retrieved_metadata["topic"], "geography")

        # --- 3. Store Embeddings in Qdrant ---
        embeddings = [
            np.random.rand(self.vector_size).tolist()
            for _ in messages
        ]

        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=i + 1,
                    vector=embeddings[i],
                    payload={
                        "session_id": self.test_session_id,
                        "role": msg["role"],
                    },
                )
                for i, msg in enumerate(messages)
            ],
            wait=True,
        )

        # --- 4. Verify Qdrant Retrieval ---
        query_vector = (
            np.array(embeddings[0]) + 0.01
        ).tolist()

        print(
            f"DEBUG: Type of qdrant_client before search: "
            f"{type(self.qdrant_client)}"
        )

        try:
            # Modern Qdrant SDK
            search_result = self.qdrant_client.search_points(
                collection_name=self.collection_name,
                vector=query_vector,
                limit=1,
                with_payload=True,
            )
        except AttributeError:
            # Fallback for older SDKs
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=1,
                with_payload=True,
            )

        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].id, 1)
        self.assertEqual(
            search_result[0].payload["role"],
            "user",
        )


if __name__ == "__main__":
    unittest.main()
