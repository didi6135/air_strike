class Mission:
    def __init__(self, target_city, priority, assigned_pilot, assigned_aircraft, distance, weather_conditions, pilot_skill, aircraft_speed, fuel_capacity):
        self.target_city = target_city
        self.priority = priority
        self.assigned_pilot = assigned_pilot
        self.assigned_aircraft = assigned_aircraft
        self.distance = distance
        self.weather_conditions = weather_conditions
        self.pilot_skill = pilot_skill
        self.aircraft_speed = aircraft_speed
        self.fuel_capacity = fuel_capacity
        self.mission_fit_score = 0

    def __repr__(self):
        return f"Mission({self.target_city}, Priority: {self.priority}, Pilot: {self.assigned_pilot}, Aircraft: {self.assigned_aircraft}, Fit Score: {self.mission_fit_score})"