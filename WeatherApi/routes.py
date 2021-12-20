from flask_restful import reqparse, Resource, abort

from WeatherApi.app import app, db, api
from WeatherApi.controller import get_weather_data, get_average_city_param, get_moving_average, get_data_range_params
from WeatherApi.models import City

CITY_NAMES = [i.city_name for i in City.query.all()]
VALUE_TYPE_NAMES = ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']


class UpdateData(Resource):
    """завантаження даних з openweathermap.org"""
    def get(self):
        return get_weather_data()


class CityList(Resource):
    """список міст в базі даних"""
    def get(self):
        return CITY_NAMES


class AverageCityParam(Resource):
    """http://localhost:5000/mean?city=kiev&value_type=pcp"""

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str, help=f'City name {CITY_NAMES}', required=True)
        parser.add_argument('value_type', type=str, help=f'Params to parse {VALUE_TYPE_NAMES}', required=True)
        args = parser.parse_args()
        if args['city'].title() in CITY_NAMES and args['value_type'] in VALUE_TYPE_NAMES:
            return get_average_city_param(args)
        else:
            return abort(404, message="incorrect value")


class DateRangeParams(Resource):
    """ http://localhost:5000/records?city=kiev&start_dt=1639904400&end_dt=1640599200 """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str, help=f'City name {CITY_NAMES}', required=True)
        parser.add_argument('start_dt', type=int, help=f'Date of start parse {VALUE_TYPE_NAMES}', required=True)
        parser.add_argument('end_dt', type=int, help=f'Date of end parse {VALUE_TYPE_NAMES}', required=True)
        args = parser.parse_args()
        if args['city'].title() in CITY_NAMES:
            return get_data_range_params(args)
        else:
            return abort(404, message="incorrect value")


class MovingAverageParams(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str, help=f'City name {CITY_NAMES}', required=True)
        parser.add_argument('value_type', type=str, help=f'Params to parse {VALUE_TYPE_NAMES}', required=True)
        args = parser.parse_args()
        if args['city'].title() in CITY_NAMES and args['value_type'] in VALUE_TYPE_NAMES:
            return get_moving_average(args)
        else:
            return abort(404, message="incorrect value")


api.add_resource(UpdateData, '/')
api.add_resource(CityList, '/cities')
api.add_resource(AverageCityParam, '/mean')
api.add_resource(DateRangeParams, '/records')
api.add_resource(MovingAverageParams, '/moving_mean')


# @app.route('/', methods=['GET', 'POST'])
# def main_page():
#     return jsonify(get_weather_data())
#
#
# @app.route('/cities', methods=['GET'])
# def get_city():
#     """список міст в базі даних"""
#     cities = City.query.all()
#     return jsonify([i.city_name for i in cities])
#
#
# @app.route('/mean/<value_type>/<city>', methods=['GET'])
# def get_average_params(value_type, city):
#     """середнє значення вибраного параметру для вибраного міста"""
#     return CITY_LIST
#
#
# @app.route('/records/<city>/<int:start_dt>/<int:end_dt>', methods=['GET'])
# def get_all_value(city, start_dt, end_dt):
#     """значення всіх параметрів для вибраного міста впродовж вибраного терміну"""
#     return CITY_LIST
#
#
# @app.route('/moving_mean/<value_type>/<city>', methods=['GET'])
# def get_moving_mean(value_type, city):
#     """значення вибраного параметру перераховане за алгоритмом ковзного середнього (moving average)
#      для вибраного міста для всіх дат"""
#     return CITY_LIST


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
