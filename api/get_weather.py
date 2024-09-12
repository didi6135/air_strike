from datetime import datetime
from operator import itemgetter

import requests
from toolz import first, pipe
from toolz.curried import partial

from repository.json_repository import read_json_by_json_name

API_KEY = 'e13e2f58860803c3d96ed87cc5d81d13'


def get_weather_data_by_city(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        return pipe(
            data['list'],
            lambda mid: filter(lambda time: time['dt_txt'] == "2024-09-13 00:00:00", mid),
            list
        )
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)



def get_weather_form_api_all_targets():
    get_weather_save = read_json_by_json_name('data/all_weather.json')
    if get_weather_save:
        return get_weather_save
    # else:
        # data = read_json_by_json_name('../data/targets.json')
        #
        # return pipe(
        #     data['targets'],
        #     partial(map, itemgetter('city')),
        #     list,  # Convert to list to ensure full evaluation
        #     lambda cities: list(map(lambda city: {city: get_weather_data_by_city(city)}, cities))
        # )


# print(get_weather_data_by_city('yemen'))
