# FlaskRestApi
 Test task for Ukrainian Hydrometeorological Institute
    
    Run:
        backend: main.py
        test requests to api: request_samples.py

    API:
        /cities [GET]

        /mean [GET]
            Params:
                value_type ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']
                city ['kiev', 'lviv', 'odesa', 'chenihiv', 'rivne']

        /records [GET]
            Params: 
                city ['kiev', 'lviv', 'odesa', 'chenihiv', 'rivne']
                start_dt [timestamp]
                end_dt [timestamp]

        /moving_mean [GET]
            Params:
                value_type ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']
                city ['kiev', 'lviv', 'odesa', 'chenihiv', 'rivne']

