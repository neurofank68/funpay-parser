import time
from typing import Tuple, Optional

import dateparser
import requests
from parsel import Selector

from database import connect_to_database, create_database_table, insert_data
from log_config import logger


def parse_user_data(user_id: int, session: requests.Session, base_url: str) -> Tuple[Optional[str], Optional[float]]:
    url = f"{base_url}/users/{user_id}/"
    nickname = None
    registration_timestamp = None

    try:
        response = session.get(url)
        response.raise_for_status()

        sel = Selector(response.text)
        nickname = sel.css('span.mr4::text').get()
        registration_date = sel.css('div.text-nowrap::text').get()

        if nickname:
            if registration_date:
                registration_timestamp = dateparser.parse(registration_date).timestamp()

    except requests.exceptions.RequestException as e:
        logger.error(f'Ошибка при запросе: {e}')
    except AttributeError as e:
        logger.error(f'Ошибка при парсинге: {e}')
    finally:
        return nickname, registration_timestamp


def parse_funpay_data():
    base_url = "https://funpay.com"

    with requests.Session() as session:
        connection = connect_to_database()
        create_database_table(connection)

        for user_id in range(1, 1001):
            nickname, registration_timestamp = parse_user_data(user_id, session, base_url)
            time.sleep(0.5)
            if nickname is not None:
                url = f"{base_url}/users/{user_id}/"
                insert_data(connection, url, nickname, registration_timestamp)
                logger.info(f'{nickname} успешно спарсен')


if __name__ == "__main__":
    time.sleep(2)
    parse_funpay_data()
