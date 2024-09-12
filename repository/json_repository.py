import json


def read_json_by_json_name(json_path):
    try:
        with open(json_path, 'r') as jsonfile:
            data = json.load(jsonfile)
            return data
    except FileNotFoundError:
        print(f"Error: The file {json_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {json_path} contains invalid JSON.")
        return None


def read_target():
    with open('data/targets.json', 'r') as file:
        data = json.load(file)
        json_formatted_str = json.dumps(data, indent=2)
        return json_formatted_str