import logging
import time

import dateparser
import requests
from parsel import Selector

from database import get_db_connection, create_database_table, insert_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

base_url = "https://funpay.com"


def parse_user_data(session: requests.Session,
                    user_url: str,
                    ) -> tuple[str, float]:
    nickname = None
    registration_timestamp = None

    try:
        response = session.get(user_url)
        response.raise_for_status()

        sel = Selector(response.text)
        nickname = sel.css('span.mr4::text').get()
        registration_date = sel.css('div.text-nowrap::text').get()

        if nickname and registration_date:
            registration_timestamp = dateparser.parse(registration_date).timestamp()

    except requests.exceptions.RequestException as e:
        logger.error(f'Ошибка при запросе: {e}')
    except AttributeError as e:
        logger.error(f'Ошибка при парсинге: {e}')
    finally:
        return nickname, registration_timestamp


def parse_funpay_data() -> None:
    with requests.Session() as session, get_db_connection() as conn:
        create_database_table(conn)

        for user_id in range(1, 1001):
            user_url = f"{base_url}/users/{user_id}/"
            nickname, registration_timestamp = parse_user_data(session, base_url)
            time.sleep(0.5)
            if nickname is not None:
                insert_data(conn,
                            user_url,
                            nickname,
                            registration_timestamp)
                logger.info(f'{nickname} успешно спарсен')


if __name__ == "__main__":
    parse_funpay_data()
