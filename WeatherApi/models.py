import loguru

from WeatherApi.app import db


class City(db.Model):
    """list of cities with geographic coordinates (Latitude, Longitude)"""
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=True, unique=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    records = db.relationship('Record', backref='city')

    def __init__(self, city_name=None, latitude=None, longitude=None):
        self.city_name = city_name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.city_name


class Record(db.Model):
    """
    :param
    date(Unix, UTC) - forecast date
    temp(°C) - average daily temperature
    pcp(mm) - precipitation for the day
    clouds(%) - clouds in the sky
    pressure(hPa) - atmospheric pressure
    humidity(%) - humidity
    wind_speed(m/s) - wind speed
    """
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    date = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    pcp = db.Column(db.Integer, default=0)
    clouds = db.Column(db.Integer, default=0)
    pressure = db.Column(db.Integer, default=0)
    humidity = db.Column(db.Integer, default=0)
    wind_speed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.city_id}:{self.date}'


def check_db_error() -> bool:
    """check errors while commit to database"""
    try:
        db.session.commit()
        return True
    except Exception as e:
        loguru.logger.error(e)
        return False


def init_db():
    """creating a database"""
    db.create_all()


def fill_city_db():
    """filling the db with city names and geographical coordinates"""
    city_list = {
                    'Kiev': {
                        'latitude': 50.450001,
                        'longitude': 30.523333,
                    },
                    'Lviv': {
                        'latitude': 49.842957,
                        'longitude': 24.031111,
                    },
                    'Odesa': {
                        'latitude': 46.482952,
                        'longitude': 30.712481,
                    },
                    'Chenihiv': {
                        'latitude': 51.493889,
                        'longitude': 31.294722,
                    },
                    'Rivne': {
                        'latitude': 50.619900,
                        'longitude': 26.251617,
                    }
                }
    for city_name, city_coords in city_list.items():
        new_city = City(city_name, city_coords['latitude'], city_coords['longitude'])
        db.session.add(new_city)
    try:
        db.session.commit()
    except Exception as e:
        loguru.logger.error(e)
