import dateparser
import pandas as pd
import requests
from bs4 import BeautifulSoup

import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/105.0.0.0 Safari/537.36'
}
data = []
for p in range(1, 10001):

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
    user_data = url, nickname, registration_timestamp
    data.append(user_data)
    print(user_data)

header = ['url', 'nickname', 'registration_timestamp']
df = pd.DataFrame(data, columns=header)
df.to_csv('funpay.csv')
