from WeatherApi import routes
from WeatherApi.models import init_db, fill_city_db

if __name__ == '__main__':
    """uncommitted 6, 7 line to initialize app"""
    # init_db()
    # fill_city_db()
    routes.app.run(host='localhost', port=5000, debug=True)
