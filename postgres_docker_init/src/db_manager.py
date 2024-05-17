# Import libraries
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Retrieve PostgreSQL credentials from environment variables.
def get_pg_creds():
    return {
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "port": os.environ.get("POSTGRES_PORT", 5434),
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "dbname": os.environ.get("POSTGRES_DB"),
    }


# Establish a connection to the PostgreSQL database.
def start_postgres_connection():
    creds = get_pg_creds()
    try:
        connection = psycopg2.connect(
            dbname=creds["dbname"],
            user=creds["user"],
            password=creds["password"],
            host=creds["host"],
            port=creds["port"],
        )
        return connection
    except psycopg2.OperationalError as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None


# Execute a SQL query on the PostgreSQL database and fetch all results.
def query_database(connection, query_str):
    try:
        cursor = connection.cursor()
        cursor.execute(query_str)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()
