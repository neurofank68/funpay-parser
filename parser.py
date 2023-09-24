import dateparser
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from config import host, user, password, db_name

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/105.0.0.0 Safari/537.36'
}

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

# Создание курсора
cur = connection.cursor()

# Создание таблицы
cur.execute("""
    CREATE TABLE IF NOT EXISTS funpay_data (
        id serial PRIMARY KEY,
        url text,
        nickname text,
        registration_timestamp double precision
    )
""")

# Закрытие курсора и сохранение изменений в базе данных
connection.commit()

# Создание курсора
cur = connection.cursor()

for p in range(1, 1001):

    url = f"https://funpay.com/users/{p}/"
    try:
        response = requests.get(url, headers=headers)
        time.sleep(0.3)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(e)
        continue

    nickname = soup.find('span', class_='mr4').text
    registration_date = soup.find('div', class_='text-nowrap').contents[0].text
    registration_timestamp = dateparser.parse(registration_date).timestamp()

    # Вставка данных в таблицу
    cur.execute("INSERT INTO funpay_data (url, nickname, registration_timestamp) VALUES (%s, %s, %s)",
                (url, nickname, registration_timestamp))
    connection.commit()

    print(f"Inserted data for {nickname}")

# Закрытие курсора и соединения
cur.close()
connection.close()