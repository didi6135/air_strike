import math
import requests
from toolz import pipe

from api.get_weather import get_weather_form_api_all_targets
from repository.json_repository import read_json_by_json_name
from service.distance_service import haversine_distance, get_location_by_ip, calculate_distances_for_targets, \
    find_max_distance
from service.normalization_service import normalize_distance
from service.weather_service import weather_score, extract_weather_info, get_weather_for_all_targets

weights = {
    "distance": 0.30,            # 20%
    "aircraft_type": 0.25,       # 25%
    "pilot_skill": 0.25,         # 25%
    "weather_conditions": 0.20,  # 20%
    # "execution_time": 0.10       # 10%
}



def preprocess_aircrafts_and_pilots():
    aircrafts = read_json_by_json_name('data/aircrafts.json')['aircrafts']
    pilots = read_json_by_json_name('data/pilots.json')['pilots']

    sorted_aircrafts = sorted(aircrafts, key=lambda a: a['speed'] / max(a['fuel_capacity'], 1), reverse=True)
    sorted_pilots = sorted(pilots, key=lambda p: p['skill'], reverse=True)

    return sorted_aircrafts, sorted_pilots


def evaluate_mission(target, pilot, aircraft, weather_condition, max_distance, your_location_lat, your_location_lon):
    # Calculate normalized distance
    distance = haversine_distance(target['lat'], target['lon'], your_location_lat, your_location_lon)
    distance_score = normalize_distance(distance, max_distance)
    aircraft_score = aircraft['speed'] / max(aircraft['fuel_capacity'], 1)

    # Pilot skill score
    pilot_skill_score = pilot['skill'] / 10  # Assuming skill is rated out of 10

    # Weather condition score
    weather_condition_score = weather_score(weather_condition)
    # Final score calculation without execution_time
    final_score = (
            distance_score * weights['distance'] +
            aircraft_score * weights['aircraft_type'] +
            pilot_skill_score * weights['pilot_skill'] +
            weather_condition_score * weights['weather_conditions']
    )

    return final_score


def find_best_missions():
    all_weather = get_weather_form_api_all_targets()
    my_location = get_location_by_ip()
    weather_data = get_weather_for_all_targets(all_weather)
    targets = read_json_by_json_name('data/targets.json')['targets']

    # Sort aircrafts and pilots
    sorted_aircrafts, sorted_pilots = preprocess_aircrafts_and_pilots()

    # Calculate distances for all targets and find the maximum distance
    distances = calculate_distances_for_targets()
    max_distance = find_max_distance(distances)

    results = []

    # Keep track of assigned targets (one per aircraft)
    available_aircrafts = sorted_aircrafts[:]
    available_pilots = sorted_pilots[:]

    for i, target in enumerate(targets):
        if not available_aircrafts or not available_pilots:
            break  # Stop when there are no more aircraft or pilots left

        # Assign the best remaining aircraft and pilot
        best_aircraft = available_aircrafts.pop(0)  # Take the best available aircraft
        best_pilot = available_pilots.pop(0)  # Take the best available pilot

        # Get the weather info for the target city
        weather_info = weather_data[i]['weather_info']
        # Calculate the mission score
        score = evaluate_mission(
            target,
            best_pilot,
            best_aircraft,
            weather_info,
            max_distance,
            float(my_location[0]),
            float(my_location[1])
        )

        result = {
            "Target City": target['city'],
            "Assigned Pilot": best_pilot['name'],
            "Assigned Aircraft": best_aircraft['type'],
            "Distance (km)": round(distances[targets.index(target)], 2),
            "Weather Conditions": weather_info.get('weather_condition', 'N/A'),
            "Pilot Skill": best_pilot['skill'],
            "Aircraft Speed (km/h)": best_aircraft['speed'],
            "Fuel Capacity (km)": best_aircraft['fuel_capacity'],
            "Mission Fit Score": round(score, 2)
        }
        results.append(result)

    return results

# def find_best_missions():
#
#     all_weather = get_weather_form_api_all_targets()
#
#     my_location = get_location_by_ip()
#     weather_data = get_weather_for_all_targets(all_weather)
#     targets = read_json_by_json_name('data/targets.json')['targets']
#     sorted_aircrafts, sorted_pilots = preprocess_aircrafts_and_pilots()
#     distances = calculate_distances_for_targets()
#     max_distance = find_max_distance(distances)
#
#     results = []
#
#
#     for i, target in enumerate(targets):
#         weather_info = weather_data[i]['weather_info']
#         best_pilot = sorted_pilots[i % len(sorted_pilots)]  # Distribute pilots evenly
#         best_aircraft = sorted_aircrafts[i % len(sorted_aircrafts)]  # Distribute aircrafts evenly
#
#         score = evaluate_mission(
#             target,
#             best_pilot,
#             best_aircraft,
#             weather_info,
#             max_distance,
#             float(my_location[0]),
#             float(my_location[1])
#         )
#
#         result = {
#             "Target City": target['city'],
#             "Assigned Pilot": best_pilot['name'],
#             "Assigned Aircraft": best_aircraft['type'],
#             "Distance (km)": round(distances[i], 2),
#             "Weather Conditions": weather_info['weather_condition'],
#             "Pilot Skill": best_pilot['skill'],
#             "Aircraft Speed (km/h)": best_aircraft['speed'],
#             "Fuel Capacity (km)": best_aircraft['fuel_capacity'],
#             "Mission Fit Score": round(score, 2)
#         }
#         # print(result, end='\n')
#
#         results.append(result)
#
#     return results



def calculate_total_score(distance_score, aircraft_score, pilot_skill_score, weather_score, execution_time_score):
    total_score = (distance_score * weights['distance'] +
                   aircraft_score * weights['aircraft_type'] +
                   pilot_skill_score * weights['pilot_skill'] +
                   weather_score * weights['weather_conditions'] +
                   execution_time_score * weights['execution_time'])
    return total_score



