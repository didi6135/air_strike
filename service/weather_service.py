from toolz import pipe, get_in
from toolz.curried import partial

from api.get_weather import get_weather_form_api_all_targets
from repository.json_repository import read_json_by_json_name

weather_conditions = {
    "Clear": 1.0,    # Best condition
    "Clouds": 0.7,   # Clouds are moderate
    "Rain": 0.4,     # Rainy weather
    "Stormy": 0.2,   # Stormy weather is least favorable
    "default": 0     # Unfavorable condition
}

def weather_score(weather):
    return weather_conditions.get(weather['weather_condition'])


def extract_weather_info(weather_data, city):

    for city_weather in weather_data:
        # print(city_weather)
        if city in city_weather:
            return pipe(
                city_weather[city][0],
                lambda wd: {
                    'weather_condition': get_in(['weather', 0, 'main'], wd, default='N/A'),
                    'cloud_coverage': get_in(['clouds', 'all'], wd, default=0),
                    'wind_speed': get_in(['wind', 'speed'], wd, default=0.0)
                }
            )

    return {
        'weather_condition': 'N/A',
        'cloud_coverage': 0,
        'wind_speed': 0.0
    }


def get_weather_for_all_targets(weather_data):

    targets = read_json_by_json_name('data/targets.json')['targets']
    all_weather_info = []

    for target in targets:
        city = target['city']
        weather_info = extract_weather_info(weather_data, city)  # Extract weather info for the city
        all_weather_info.append({
            "city": city,
            "weather_info": weather_info
        })

    return all_weather_info


# Test with 'Damascus'
# all_weather = get_weather_form_api_all_targets()
#
# # Extract weather info for 'Damascus'
# print(get_weather_for_all_targets(all_weather))
# def get_detail_from_weather_that_need_for_calc():

    # all_weather = get_weather_for_all_targets()

