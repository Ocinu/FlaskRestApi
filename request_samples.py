import random
import time
import datetime

import requests
import json

CITY_NAMES = ['kiev', 'lviv', 'odesa', 'chenihiv', 'rivne']
VALUE_TYPE_NAMES = ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']


def load_data():
    """refresh db data for next 7 days"""
    response = requests.get('http://localhost:5000')
    if 200 <= response.status_code <= 299:
        return True
    return False


def request_city_list():
    url = f'http://localhost:5000/cities'
    response = requests.get(url)
    print(f'Список назв міст у базі даних:\n{json.dumps(json.loads(response.content), indent=2)}\n\n')


def request_mean():
    city = random.choice(CITY_NAMES)
    value_type = random.choice(VALUE_TYPE_NAMES)
    url = f'http://localhost:5000/mean?city={city}&value_type={value_type}'
    response = requests.get(url)
    print(f'Cереднє значення вибраного параметру для вибраного міста:\n'
          f'{json.dumps(json.loads(response.content), indent=2)}\n\n')


def request_records():
    city = random.choice(CITY_NAMES)
    start_dt = "20/12/2021"
    end_dt = "22/12/2021"
    url = f'http://localhost:5000/records?city={city}&start_dt={get_timestamp(start_dt)}&end_dt={get_timestamp(end_dt)}'
    response = requests.get(url)
    print(f'Значення всіх параметрів для вибраного міста впродовж вибраного терміну\n'
          f'{json.dumps(json.loads(response.content), indent=2)}\n\n')


def request_moving_mean():
    city = random.choice(CITY_NAMES)
    value_type = random.choice(VALUE_TYPE_NAMES)
    url = f'http://localhost:5000/mean?city={city}&value_type={value_type}'
    response = requests.get(url)
    print(f'Значення вибраного параметру перераховане за алгоритмом ковзного середнього\n'
          f'{json.dumps(json.loads(response.content), indent=2)}')


def get_timestamp(data: str) -> int:
    return round(int(time.mktime(datetime.datetime.strptime(data, "%d/%m/%Y").timetuple())))


def main():
    if load_data():
        request_city_list()
        request_mean()
        request_records()
        request_moving_mean()
    else:
        print('Check backend app')


if __name__ == '__main__':
    main()
