import os
import time

import dateparser
import requests
from parsel import Selector

from database import connect_to_database, create_database_table, insert_data
from logger_info import logger

if 'DOCKER_CONTAINER' in os.environ:
    DB_HOST = "database"
else:
    DB_HOST = "localhost"

def parse_user_data(user_id, session):
    url = f"https://funpay.com/users/{user_id}/"

    try:
        response = session.get(url)
        response.raise_for_status()

        sel = Selector(response.text)
        nickname = sel.css('span.mr4::text').get()
        registration_date = sel.css('div.text-nowrap::text').get()

        if nickname and registration_date:
            registration_timestamp = dateparser.parse(registration_date).timestamp()
            return nickname, registration_timestamp
        else:
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error(f'Ошибка при запросе: {e}')
        return None, None
    except AttributeError as e:
        logger.error(f'Ошибка при парсинге: {e}')
        return None, None

def parse_funpay_data():
    with requests.Session() as session:
        connection = connect_to_database()
        create_database_table(connection)

        for user_id in range(1, 1001):
            nickname, registration_timestamp = parse_user_data(user_id, session)
            time.sleep(0.3)
            if nickname is not None:
                url = f"https://funpay.com/users/{user_id}/"
                insert_data(connection, url, nickname, registration_timestamp)
                logger.info(f'{nickname} успешно спарсен')

        connection.close()


if __name__ == "__main__":
    parse_funpay_data()
