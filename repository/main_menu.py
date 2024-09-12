from repository.csv_repository import save_mission_data_to_csv
from repository.json_repository import read_json_by_json_name, read_target
from service.calc_best_solution import find_best_missions



def print_options():
    data = None  # To store loaded data
    while True:
        print("\nMenu:")
        print("1. Load JSON files (Targets and all other information)")
        print("2. Display recommendation table for attacks")
        print("3. Save all attack data to a CSV file")
        print("4. Exit")

        choice = input("Please select an option (1-4): ")

        if choice == '1':
            data = read_target()
            print(data)
        elif choice == '2':
            all_mission = find_best_missions()
            for mission in all_mission:
                print(mission, end='\n')
        elif choice == '3':
            all_mission = find_best_missions()
            save_mission_data_to_csv(all_mission, 'data/missions_report.csv')
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please select again.")
