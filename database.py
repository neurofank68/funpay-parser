import os
import psycopg2
from psycopg2.extensions import connection

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_NAME = os.getenv('POSTGRES_NAME', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)


class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg2.connect(
            host=POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_NAME,
            port=POSTGRES_PORT
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def create_database_table(conn: connection) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS funpay_data (
                id serial PRIMARY KEY,
                url text,
                nickname text,
                registration_timestamp double precision
            )
    """)
    conn.commit()


def insert_data(
        conn: connection,
        url: str,
        nickname: str,
        registration_timestamp: float,
) -> None:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO funpay_data (url, nickname, registration_timestamp) VALUES (%s, %s, %s)",
                    (url, nickname, registration_timestamp))
    conn.commit()
