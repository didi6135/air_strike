
weather_conditions = {
    "Clear": 1.0,    # Best condition
    "Clouds": 0.7,   # Clouds are moderate
    "Rain": 0.4,     # Rainy weather
    "Stormy": 0.2,   # Stormy weather is least favorable
    "default": 0     # Unfavorable condition
}


def normalize_distance(distance, max_distance):
    return 1 - (distance / max_distance)

def normalize_pilot_skills(skill, max_skill=10):
    return skill / max_skill

def normalize_weather(weather_condition):
    return weather_conditions.get(weather_condition, weather_conditions['default'])

def normalize_execution_time(execution_time, earliest_time, latest_time):
    return 1 - ((execution_time - earliest_time) / (latest_time - earliest_time))
