import time
import numpy as np

import loguru
import requests
from sqlalchemy import inspect

from WeatherApi.app import db
from WeatherApi.models import City, Record, check_db_error
from config import WEATHER_API_KEY


def get_weather_data() -> dict:
    """getting a seven-day weather forecast for all cities from the openweathermap.org"""
    cities = City.query.all()
    global_weather_params = {'Kiev': {'data': {}}}
    for city in cities:
        part = 'minutely,hourly'
        units = 'metric'
        weather_url = f'https://api.openweathermap.org/data/2.5/onecall?' \
                      f'lat={city.latitude}&' \
                      f'lon={city.longitude}&' \
                      f'exclude={part}&' \
                      f'units={units}&' \
                      f'appid={WEATHER_API_KEY}'
        try:
            weather_data = requests.get(weather_url)
        except Exception as e:
            weather_data = {'error': e}
            loguru.logger.error(e)
        if 200 <= weather_data.status_code <= 299:
            global_weather_params[city.city_name] = get_weather_params(city, weather_data.json())
        else:
            global_weather_params[city.city_name] = {'error': weather_data.status_code}
    return global_weather_params


def get_weather_params(city: City, weather_data: dict) -> dict:
    """extracting desired parameters from shared data"""
    city_weather_params = {}
    for day_data in weather_data['daily']:
        if save_record(city, day_data):
            city_weather_params[get_hf_data(day_data["dt"])] = {
                'temp': get_average_temp(day_data["temp"]),
                'pcp': day_data["pop"],
                'clouds': day_data["clouds"],
                'pressure': day_data["pressure"],
                'humidity': day_data["humidity"],
                'wind_speed': day_data["wind_speed"]
            }
        else:
            city_weather_params[get_hf_data(day_data["dt"])] = {
                'error': 'error save data to db'
            }
    return city_weather_params


def get_average_city_param(args: dict) -> dict:
    """return average value of the selected parameter for the selected city"""
    city = City.query.filter_by(city_name=args['city'].title()).first()
    rec_list = get_city_params_list(city, args['value_type'])
    if rec_list[0] == 'error':
        return {"message": {"error": rec_list[1]}}
    return {city.city_name: {args['value_type']: round(int(np.mean(rec_list)), 2)}}


def get_data_range_params(args: dict) -> dict:
    """return all value for selected range of data for selected city"""
    city = City.query.filter_by(city_name=args['city'].title()).first()
    records = Record.query.filter_by(city_id=city.id).filter(Record.date >= args['start_dt']).filter(
        Record.date <= args['end_dt']).order_by(db.asc(Record.date)).all()
    result = {city.city_name: {}}
    for record in records:
        result[city.city_name][get_hf_data(record.date)] = {
            'temp': record.temp,
            'pcp': record.pcp,
            'clouds': record.clouds,
            'pressure': record.pressure,
            'humidity': record.humidity,
            'wind_speed': record.wind_speed
        }
    return result


def get_moving_average(args: dict) -> dict:
    """return moving average value of the selected parameter for the selected city"""
    city = City.query.filter_by(city_name=args['city'].title()).first()
    rec_list = get_city_params_list(city, args['value_type'])
    if rec_list[0] == 'error':
        return {"message": {"error": rec_list[1]}}
    moving_average_value = moving_average(rec_list)
    return {'city': city.city_name, args['value_type']: moving_average_value}


def moving_average(value_list: list) -> float:
    """return moving average value for list of value_list"""
    data = np.array(value_list)
    moving_average_value = np.convolve(data, np.ones(len(value_list)), 'valid') / len(value_list)
    return round(moving_average_value.tolist()[0], 2)


def get_city_params_list(city: City, value_type: str) -> list:
    """return list of values of the selected parameter for the selected city"""
    records = city.records
    rec_list = []
    for record in records:
        try:
            value = getattr_from_column_name(record, value_type, default=Ellipsis)
        except Exception as e:
            loguru.logger.error(e)
            rec_list = ['error', e]
            return rec_list
        rec_list.append(value)
    return rec_list


def getattr_from_column_name(instance, name, default=Ellipsis):
    """getting the value of a column by its name"""
    for attr, column in inspect(instance.__class__).c.items():
        if column.name == name:
            return getattr(instance, attr)

    if default is Ellipsis:
        raise KeyError
    else:
        return default


def get_hf_data(data: int) -> str:
    """convert data to human friendly visible"""
    local_time = time.localtime(data)
    forecast_data = f'{local_time.tm_year}:{local_time.tm_mon}:{local_time.tm_mday}'
    return forecast_data


def get_average_temp(data: dict) -> float:
    """average daily temperature"""
    average_temp = (data['min'] + data['max']) / 2
    return round(average_temp, 2)


def save_record(city: City, day_data: dict) -> bool:
    """adds an entry if it does not exist, otherwise it updates the data"""
    record = Record.query.filter(Record.city_id == city.id).filter(Record.date == day_data["dt"]).all()
    if len(record) == 0:
        new_record = Record()
        new_record.city_id = city.id
        new_record.date = day_data["dt"]
        new_record.temp = get_average_temp(day_data["temp"])
        new_record.pcp = day_data["pop"]
        new_record.clouds = day_data["clouds"]
        new_record.pressure = day_data["pressure"]
        new_record.humidity = day_data["humidity"]
        new_record.wind_speed = day_data["wind_speed"]
        db.session.add(new_record)
        return check_db_error()
    elif len(record) == 1:
        update_record = record[0]
        update_record.temp = get_average_temp(day_data["temp"])
        update_record.pcp = day_data["pop"]
        update_record.clouds = day_data["clouds"]
        update_record.pressure = day_data["pressure"]
        update_record.humidity = day_data["humidity"]
        update_record.wind_speed = day_data["wind_speed"]
        return check_db_error()
    else:
        return False
