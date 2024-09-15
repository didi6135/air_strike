from datetime import datetime, timedelta
from operator import itemgetter
import json
import os
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

        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00"
        return pipe(
            data['list'],
            # lambda mid: filter(lambda time: time['dt_txt'] == "2024-09-13 00:00:00", mid),
            lambda mid: filter(lambda time: time['dt_txt'] == tomorrow_date, mid),
            list
        )
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


# Fetch weather data for all targets and save them to a file
def fetch_weather_for_all_targets():
    target_cities = read_json_by_json_name('data/targets.json')['targets']

    all_weather_data = []
    for target in target_cities:
        city = target['city']
        weather_data = get_weather_data_by_city(city)
        if weather_data:
            all_weather_data.append({city: weather_data})

    # Save the weather data into a JSON file
    with open('data/all_weather.json', 'w') as jsonfile:
        json.dump(all_weather_data, jsonfile, indent=4)

    return all_weather_data


# Load weather data from the JSON file if it exists, else fetch from API and save
def get_weather_form_api_all_targets():
    file_path = 'data/all_weather.json'
    try:
        # If the file exists, read and return its content
        if os.path.exists(file_path):
            print("Loading weather data from the saved file...")
            with open(file_path, 'r') as jsonfile:
                weather_data = json.load(jsonfile)
                return weather_data
        else:
            # If the file does not exist, fetch from the API
            print("Weather data not found locally, fetching from API...")
            return fetch_weather_for_all_targets()

    except FileNotFoundError:
        # If there's an error loading the file, fetch data from API
        print("Weather data not found, fetching from API...")
        return fetch_weather_for_all_targets()

    # return None  # Handle case if no data was retrieved


# def get_weather_form_api_all_targets():
#     get_weather_save = read_json_by_json_name('data/all_weather2.json')
#     if get_weather_save:
#         return get_weather_save
#     # else:
#         # data = read_json_by_json_name('../data/targets.json')
#         #
#         # return pipe(
#         #     data['targets'],
#         #     partial(map, itemgetter('city')),
#         #     list,  # Convert to list to ensure full evaluation
#         #     lambda cities: list(map(lambda city: {city: get_weather_data_by_city(city)}, cities))
#         # )


# print(get_weather_data_by_city('yemen'))
