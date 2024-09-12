import csv
import os


def save_mission_data_to_csv(missions, csv_file_path):
    # Ensure the 'data' folder exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Define the CSV column headers
    headers = ["Target City", "Assigned Pilot", "Assigned Aircraft", "Distance (km)",
               "Weather Conditions", "Pilot Skill", "Aircraft Speed (km/h)",
               "Fuel Capacity (km)", "Mission Fit Score"]

    try:
        # Open the CSV file for writing
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            # Write the header to the CSV
            writer.writeheader()

            # Write each mission's data as a row in the CSV
            for mission in missions:
                writer.writerow({
                    "Target City": mission["Target City"],
                    "Assigned Pilot": mission["Assigned Pilot"],
                    "Assigned Aircraft": mission["Assigned Aircraft"],
                    "Distance (km)": mission["Distance (km)"],
                    "Weather Conditions": mission["Weather Conditions"],
                    "Pilot Skill": mission["Pilot Skill"],
                    "Aircraft Speed (km/h)": mission["Aircraft Speed (km/h)"],
                    "Fuel Capacity (km)": mission["Fuel Capacity (km)"],
                    "Mission Fit Score": mission["Mission Fit Score"]
                })

        print(f"Mission data successfully saved to {csv_file_path}")
    except Exception as e:
        print(f"Error saving mission data to CSV: {e}")
