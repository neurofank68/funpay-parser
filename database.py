import psycopg2
from decouple import config
def connect_to_database():
    DB_HOST = config('DB_HOST')
    DB_NAME = config('DB_NAME')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_PORT = config('DB_PORT')

    connection = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

    return connection

def create_database_table(connection):
    cur = connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS funpay_data (
            id serial PRIMARY KEY,
            url text,
            nickname text,
            registration_timestamp double precision
        )
    """)
    connection.commit()
    cur.close()

def insert_data(connection, url, nickname, registration_timestamp):
    cur = connection.cursor()
    cur.execute("INSERT INTO funpay_data (url, nickname, registration_timestamp) VALUES (%s, %s, %s)",
                (url, nickname, registration_timestamp))
    connection.commit()
    cur.close()

