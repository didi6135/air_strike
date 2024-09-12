import math

import requests

from repository.json_repository import read_json_by_json_name


# function to get my lat and lan
def get_location_by_ip():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    location = data['loc'].split(',')
    latitude = location[0]
    longitude = location[1]
    return latitude, longitude


# Function to calculate the distance between two coordinates using the Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0 # Radius of the Earth in kilometers
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Calculate the distance
    distance = r * c
    return distance



def calculate_distances_for_targets():
    distances = []
    targets = read_json_by_json_name('data/targets.json')
    my_location = get_location_by_ip()

    for target in targets['targets']:
        distance = haversine_distance(float(my_location[0]), float(my_location[1]), target['lat'], target['lon'])
        distances.append(distance)

    return distances



def find_max_distance(distances):
    return max(distances)

