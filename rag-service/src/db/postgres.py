import psycopg2
from psycopg2 import OperationalError
from .config import settings # Import settings from the centralized config

def get_postgres_connection():
    """
    Establishes and returns a connection to the Neon Serverless Postgres database.
    Connection settings are loaded from the centralized config.
    """
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_URL,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            dbname=settings.POSTGRES_DB
        )
        print("Successfully connected to PostgreSQL.")
        return conn
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    try:
        conn = get_postgres_connection()
        if conn:
            # You can perform some database operations here
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                db_version = cur.fetchone()
                print(f"PostgreSQL database version: {db_version}")
            conn.close()
            print("PostgreSQL connection closed.")
    except OperationalError as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")