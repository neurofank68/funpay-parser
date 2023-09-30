import os

import psycopg2


POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_NAME = os.getenv('POSTGRES_NAME', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)


def connect_to_database():
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_NAME,
        port=POSTGRES_PORT
    )

    return connection


def create_database_table(connection):
    with connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS funpay_data (
                id serial PRIMARY KEY,
                url text,
                nickname text,
                registration_timestamp double precision
            )
    """)
    connection.commit()


def insert_data(connection, url, nickname, registration_timestamp):
    with connection.cursor() as cur:
        cur.execute("INSERT INTO funpay_data (url, nickname, registration_timestamp) VALUES (%s, %s, %s)",
                    (url, nickname, registration_timestamp))
    connection.commit()
